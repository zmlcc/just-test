from . import main

from ..model import db, User

@main.route("/info")
def hello():
    return "Hello world!"


@main.route("/user/<string:name>", methods=["POST"])
def addUser(name):
    user = User(name)
    db.session().add(user)
    db.session().commit()
    return "add user {}".format(name)
