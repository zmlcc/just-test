from . import main

from ..model import db, User, Project
from ..principal import create_user_permission


@main.route("/info")
def hello():
    return "Hello world!"


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
