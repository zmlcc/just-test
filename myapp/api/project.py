from flask import jsonify, request, g, current_app
from . import api

from ..model import db, Project, User, Namespace, Cluster



from cerberus import Validator


from sqlalchemy import exc


from .. import k8sclient as k8s

from sqlalchemy.orm import defer

@api.route("/project", methods=["GET"])
def get_project():
    prj = Project.query.join(Project.user).filter(User.name==g.cur_user_name).all()
    if 0 == len(prj):
        return "", 400
    output = [item.name for item in prj]
    return jsonify(output)


project_schema = {
    "name": {
        'required': True,
        'type': 'string'
    }
}

@api.route("/project", methods=["POST"])
def add_project():
    if g.cur_user_name is None:
        return "", 400
    
    input = request.get_json()
    if input is None:
        return "", 400
    v = Validator(project_schema, allow_unknown = True)
    if not v.validate(input):
        return "", 400

    prj = Project()
    prj.name = input["name"]
    try:
        user = User.query.filter_by(name=g.cur_user_name).first()
        prj.user.append(user)
        db.session().add(prj)
        db.session().commit()
    except exc.SQLAlchemyError:
        return "", 400

    return "", 204



@api.route("/project/<prj_name>/user", methods=["GET"])
def get_project_user(prj_name):
    prj = Project.query.join(Project.user).filter(User.name==g.cur_user_name).filter(Project.name==prj_name).first()

    if prj is None:
        return "", 400
    output = [item.name for item in prj.user]
    return jsonify(output)


@api.route("/project/<prj_name>/user/<user_name>", methods=["POST"])
def add_project_user(prj_name, user_name):
    prj = Project.query.join(Project.user).filter(User.name==g.cur_user_name).filter(Project.name==prj_name).first()
    if prj is None:
        return "", 400
    user = User.query.filter(User.name==user_name).first()
    if user is None:
        return "", 400
    try:
        prj.user.append(user)
        db.session().commit() 
    except exc.SQLAlchemyError:
        return "", 400

    return "", 200


@api.route("/project/<prj_name>/cluster", methods=["GET"])
def get_project_cluster(prj_name):
    prj = Project.query.join(Project.user).filter(User.name==g.cur_user_name).filter(Project.name==prj_name).first()
    if prj is None:
        return "", 400
    
    q = Namespace.query.join(Namespace.project, Namespace.cluster).filter(Project.name==prj_name).with_entities(Cluster.name)
    output = [item[0] for item in q ]
    return jsonify(output)

@api.route("/project/<prj_name>/cluster/<cluster_name>", methods=["POST"])
def bind_project_cluster(prj_name, cluster_name):
    prj = Project.query.join(Project.user).filter(User.name==g.cur_user_name).filter(Project.name==prj_name).first()
    if prj is None:
        return "", 400
    
    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    cli = k8s.get_cli(cluster_name)
    if cli is None:
        return "", 400

    create_ns = create_namespace
    create_ns = create_namespace_wrapper(cli, prj_name)(create_ns)
    rsp = create_ns(prj, cluster)
    if rsp is None:
        return "", 400

    return "", 204


def create_namespace(prj, cluster):
    ns = Namespace()
    ns.project  = prj
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
