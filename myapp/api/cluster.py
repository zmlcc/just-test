from flask import jsonify, request, g
from . import api

from ..model import db, Cluster, Namespace, User, Project, Account

from cerberus import Validator
from sqlalchemy.orm import load_only

@api.route("/cluster", methods=['GET'])
def get_all_cluster():
    try:
        output = []
        for item in Cluster.query.with_entities(Cluster.name):
            output.append(
                {
                    "name": item[0]
                }
            )
    except:
        return "", 500
    else:
        return jsonify(output)


@api.route("/cluster/<cluster_name>", methods=["GET"])
def get_cluster(cluster_name):
    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    output = dict(
        name=cluster.name,
        addr=cluster.addr,
        cert=cluster.cert,
    )
    return jsonify(output)


@api.route("/cluster/<cluster_name>/namespace", methods=["GET"])
def get_cluster_namespace(cluster_name):
    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    subq = Project.query.join(Project.user).filter(User.name==g.cur_user_name).options(load_only("id")).subquery()
    ns = Namespace.query.join(Namespace.cluster).join(subq).filter(Cluster.name==cluster_name)

    if ns is None:
        return "", 400

    output = [ item.project.name for item in ns]

    return jsonify(output)

