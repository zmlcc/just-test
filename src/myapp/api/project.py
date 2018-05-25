from flask import jsonify, request, g, current_app
from sqlalchemy import exc
from cerberus import Validator
from . import api

from ..model import db, Project, User, Namespace, Cluster

from .. import k8s

from .util import o2prj, o2user


@api.route("/project", methods=["GET"])
def get_project():
    if g.cur_user is None:
        return "", 400

    prj = Project.query.filter(Project.user.contains(g.cur_user)).all()

    output = [o2prj(item) for item in prj]
    return jsonify(output)


project_schema = {
    "name": {
        'required': True,
        'type': 'string',
        'regex': "^prj-[a-zA-Z][a-zA-Z0-9_.+-]*"
    }
}


@api.route("/project", methods=["POST"])
def add_project():
    if g.cur_user is None:
        return "", 400

    req = request.get_json()
    current_app.logger.debug(req)
    if req is None:
        return "", 400
    v = Validator(project_schema, allow_unknown=True)
    if not v.validate(req):
        return "", 400

    if len(g.cur_user.project) >= g.cur_user.project_quota:
        return "", 403

    prj = Project()
    prj.name = req["name"]
    try:
        prj.user.append(g.cur_user)
        db.session.add(prj)  # pylint: disable=e1101
        db.session.commit()  # pylint: disable=e1101
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)
        return "", 409

    return "", 204


@api.route("/project/<prj_name>/user", methods=["GET"])
def get_project_user(prj_name):
    if g.cur_user is None:
        return "", 400

    prj = Project.query.filter(Project.user.contains(
        g.cur_user)).filter(Project.name == prj_name).first()

    if prj is None:
        return "", 400
    output = [o2user(item) for item in prj.user]
    return jsonify(output)


@api.route("/project/<prj_name>/user/<user_name>", methods=["POST"])
def add_project_user(prj_name, user_name):
    if g.cur_user is None:
        return "", 400
    prj = Project.query.filter(Project.user.contains(
        g.cur_user)).filter(Project.name == prj_name).first()
    if prj is None:
        return "", 400
    user = User.query.filter(User.name == user_name).first()
    if user is None:
        return "", 400
    try:
        prj.user.append(user)
        db.session.commit()  # pylint: disable=e1101
    except exc.SQLAlchemyError:
        return "", 400

    return "", 200


@api.route("/project/<prj_name>/cluster", methods=["GET"])
def get_project_cluster(prj_name):
    if g.cur_user is None:
        return "", 400
    prj = Project.query.filter(Project.user.contains(
        g.cur_user)).filter(Project.name == prj_name).first()
    if prj is None:
        return "", 400

    q = Namespace.query.join(
        Namespace.project,
        Namespace.cluster).filter(Project.name == prj_name).with_entities(
            Cluster.name)
    output = [dict(name=(item[0])) for item in q]
    return jsonify(output)


@api.route("/project/<prj_name>/cluster/<cluster_name>", methods=["POST"])
def bind_project_cluster(prj_name, cluster_name):
    if g.cur_user is None:
        return "", 400
    prj = Project.query.filter(Project.user.contains(
        g.cur_user)).filter(Project.name == prj_name).first()
    if prj is None:
        return "", 400

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    cli = k8s.get_cli(cluster_name)
    if cli is None:
        return "", 400

    create_ns = create_namespace_indb
    create_ns = create_namespace_wrapper(cli, prj_name)(create_ns)
    rsp = create_ns(prj, cluster)
    if rsp is None:
        return "", 400

    return "", 204


def create_namespace_indb(prj, cluster):
    ns = Namespace()
    ns.project = prj
    ns.cluster = cluster

    try:
        db.session.add(ns)  # pylint: disable=e1101
        db.session.commit()  # pylint: disable=e1101
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
