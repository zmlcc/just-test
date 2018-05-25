from flask import jsonify, request, g, current_app

from cerberus import Validator

from sqlalchemy import exc

from . import api
from ..model import db, User
from .util import o2prj, o2role

from ..principal import prin


@api.route("/whoami", methods=['GET'])
def whoami():
    current_app.logger.error(current_app.before_request_funcs["api"][0])
    current_app.logger.error(prin.identity_loaders)
    current_app.logger.error(g)
    output = dict(
        username=request.headers.get("Remote-User", ""),
        registered=False if g.cur_user is None else True)
    return jsonify(output)


@api.route("/user", methods=['GET'])
def get_all_user():
    output = []
    try:
        for item in User.query.with_entities(User.name):
            output.append({"name": item[0]})
    except:
        return "", 500

    return jsonify(output)


@api.route("/user/<username>", methods=["GET"])
def get_user(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        return "", 400

    output = dict(
        name=user.name,
        project=[o2prj(item) for item in user.project],
        role=[o2role(item) for item in user.role],
        project_quota=user.project_quota,
    )
    return jsonify(output)


user_schema = {
    "name": {
        'required': True,
        'type': 'string',
        'empty': False
    },
    "email": {
        "type": "string"
    }
}


@api.route("/user", methods=["POST"])
def creat_user():
    req = request.get_json()
    if req is None:
        return "", 400
    v = Validator(user_schema, allow_unknown=True)
    if not v.validate(req):
        return "", 400

    user = User()
    user.name = req["name"]
    user.project_quota = current_app.config.get("PROJECT_QUOTA", 1)
    # if "email" in req:
    #     pass
    try:
        db.session.add(user)  # pylint: disable=e1101
        db.session.commit()  # pylint: disable=e1101
    except exc.SQLAlchemyError:
        return "", 400

    return "", 204
