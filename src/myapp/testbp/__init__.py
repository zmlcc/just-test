from flask import Blueprint, abort, g
from ..principal import  create_user_permission

testbp = Blueprint('testbp', __name__)

@testbp.before_request
def check_user():
    if not create_user_permission.can():
        abort(404, "{}, {}".format(create_user_permission, g.identity))



@testbp.route("/test")
def hehe():
    return "hehe"

@testbp.route("/ttt")
def c2():
    return "reetettttttttttt"