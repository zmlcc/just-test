from flask import jsonify, request, g, current_app
from sqlalchemy import exc
from cerberus import Validator
from . import api

from ..model import db, Project, User, Namespace, Cluster

from .. import k8s

from .util import NS_BASE_ROLE
from .util import o2prj, o2user
from ..principal import mananger_permission


@api.route("/project", methods=["GET"])
def get_project():
    if g.cur_user is None:
        return "", 400

    prj = Project.query.filter(Project.user.contains(g.cur_user)).all()
    if 0 == len(prj):
        return "", 204
    output = [o2prj(item) for item in prj]
    return jsonify(output)


project_schema = {"name": {'required': True, 'type': 'string'}}



@api.route("/project", methods=["POST"])
@mananger_permission.require(403)
def add_project():
    if g.cur_user is None:
        return "", 400

    input = request.get_json()
    current_app.logger.info(input)
    if input is None:
        return "", 400
    v = Validator(project_schema, allow_unknown=True)
    if not v.validate(input):
        return "", 400

    prj = Project()
    prj.name = input["name"]
    try:
        prj.user.append(g.cur_user)
        db.session().add(prj)
        db.session().commit()
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)
        return "", 409

    return "", 204


@api.route("/project/<prj_name>/user", methods=["GET"])
def get_project_user(prj_name):
    if g.cur_user is None:
        return "", 400

    prj = Project.query.filter(Project.user.contains(g.cur_user)).filter(Project.name == prj_name).first()

    if prj is None:
        return "", 400
    output = [o2user(item) for item in prj.user]
    return jsonify(output)


@api.route("/project/<prj_name>/user/<user_name>", methods=["POST"])
@mananger_permission.require(403)
def add_project_user(prj_name, user_name):
    if g.cur_user is None:
        return "", 400
    prj = Project.query.filter(Project.user.contains(g.cur_user)).filter(Project.name == prj_name).first()
    if prj is None:
        return "", 400
    user = User.query.filter(User.name == user_name).first()
    if user is None:
        return "", 400
    try:
        prj.user.append(user)
        db.session().commit()
    except exc.SQLAlchemyError:
        return "", 400

    return "", 200


@api.route("/project/<prj_name>/cluster", methods=["GET"])
@mananger_permission.require(403)
def get_project_cluster(prj_name):
    if g.cur_user is None:
        return "", 400
    prj = Project.query.filter(Project.user.contains(g.cur_user)).filter(Project.name == prj_name).first()
    if prj is None:
        return "", 400

    q = Namespace.query.join(
        Namespace.project,
        Namespace.cluster).filter(Project.name == prj_name).with_entities(
            Cluster.name)
    output = [dict(name=(item[0])) for item in q]
    return jsonify(output)


@api.route("/project/<prj_name>/cluster/<cluster_name>", methods=["POST"])
@mananger_permission.require(403)
def bind_project_cluster(prj_name, cluster_name):
    if g.cur_user is None:
        return "", 400
    prj = Project.query.filter(Project.user.contains(g.cur_user)).filter(Project.name == prj_name).first()
    if prj is None:
        return "", 400

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    cli = k8s.get_cli(cluster_name)
    if cli is None:
        return "", 400

    create_ns = create_namespace_in_db
    create_ns = create_role_wrapper(cli, prj_name, NS_BASE_ROLE)(create_ns)
    create_ns = create_namespace_wrapper(cli, prj_name)(create_ns)
    rsp = create_ns(prj, cluster)
    if rsp is None:
        return "", 400

    return "", 204


def create_namespace_in_db(prj, cluster):
    ns = Namespace()
    ns.project = prj
    ns.cluster = cluster

    try:
        db.session().add(ns)
        db.session().commit()
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)
        return None

    return True


def create_namespace_wrapper(cli, name):
    def wrapper(func):
        def _wrapper(*args, **kargs):
            rsp = k8s.create_namespace(cli, name)
            if rsp is None:
                return None

            rsp = func(*args, **kargs)
            if rsp is None:
                k8s.delete_namespace(cli, name)

            return rsp

        return _wrapper

    return wrapper


def create_role_wrapper(cli, namespace, role):
    def wrapper(func):
        def _wrapper(*args, **kargs):
            rsp = k8s.create_role(cli, namespace, role)
            if rsp is None:
                return None

            rsp = func(*args, **kargs)
            if rsp is None:
                k8s.delete_role(cli, namespace, role.metadata.name)

            return rsp

        return _wrapper

    return wrapper