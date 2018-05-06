from flask import jsonify, request, g
from . import api

from ..model import db, Project, User

from cerberus import Validator


from flask_sqlalchemy import get_debug_queries


@api.route("/project", methods=["GET"])
def get_project():
    prj = Project.query.filter(User.name==g.cur_user_name).all()
    if 0 == len(prj):
        return "", 400
    output = [item.name for item in prj]
    return jsonify(output)


@api.route("/project/<prj_name>/user", methods=["GET"])
def get_project_user(prj_name):
    prj = Project.query.join(Project.user).filter(User.name==g.cur_user_name).filter(Project.name==prj_name).first()
    # prj = Project.query.filter(Project.user.any(name=g.cur_user_name)).filter(Project.name==prj_name).first()
    # for query in get_debug_queries():
    #     print(query)
    #     print()
    #     print()
    if prj is None:
        return "", 400
    output = [item.name for item in prj.user]
    return jsonify(output)


@api.route("/project/<prj_name>/user/<user_name>", methods=["POST"])
def add_project_user(prj_name, user_name):
    prj = Project.query.filter(User.name==g.cur_user_name).filter(Project.name==prj_name).first()
    if prj is None:
        return "", 400
    user = User.query.filter(User.name==user_name).first()
    if user is None:
        return "", 400
    prj.user.append(user)
    db.session.commit()
    return "", 200