from flask import jsonify
from . import main

from ..model import db, User, Project
from ..principal import create_user_permission

from ..k8s import get_cli
from kubernetes.client import CoreV1Api

@main.route("/info")
def hello():
    return "Hello world!"


@main.route("/hehe")
def hehe():
    cli = get_cli("a1")
    if cli is None:
        return "Not found cluster a1"
    api = CoreV1Api(cli)
    vv = api.list_namespaced_pod(namespace="prj-labu")
    print(vv)
    # print(type(vv))
    return jsonify(vv.to_dict())


@main.route("/user/<string:name>", methods=["POST"])
@create_user_permission.require(404)
def addUser(name):
    user = User(name)
    db.session().add(user)
    db.session().commit()
    return "add user {}".format(name)


@main.route("/project/<string:name>", methods=["POST"])
def addProject(name):
    prj = Project(name)
    db.session().add(prj)
    db.session().commit()
    return "add project {}".format(name)


@main.route(
    "/project/<string:prjname>/user/<string:username>", methods=["POST"])
def addProjectUser(prjname, username):
    prj = Project.query.filter_by(name=prjname).first()
    user = User.query.filter_by(name=username).first()
    prj.user = [user]
    db.session().add(prj)
    db.session().commit()
    return "add project user {}".format(username)
