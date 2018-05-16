from flask import jsonify, request
from . import api

from ..model import db, User

from cerberus import Validator

from sqlalchemy import exc

from .util import o2prj, o2user, o2role

@api.route("/user", methods=['GET'])
def get_all_user():
    output = []
    try:
        for item in User.query.with_entities(User.name):
            output.append(
                {
                    "name": item[0]
                }
            )
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
    )
    return jsonify(output)




user_schema = {
    "name": {
        'required': True,
        'type': 'string'
    },
    "email": {
        "type": "string"
    }
}


@api.route("/user", methods=["POST"])
def creat_user():
    input = request.get_json()
    if input is None:
        return "", 400
    v = Validator(user_schema, allow_unknown = True)
    if not v.validate(input):
        return "", 400

    user = User()
    user.name = input["name"]
    # if "email" in input:
    #     pass
    try:
        db.session().add(user)
        db.session().commit()
    except exc.SQLAlchemyError:
        return "", 400

    return "", 204
