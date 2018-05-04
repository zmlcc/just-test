from flask import jsonify, request
from . import api

from ..model import db, Cluster

from cerberus import Validator

from sqlalchemy import exc


@api.route("/cluster", methods=['GET'])
def get_all_cluster():
    try:
        output = [item[0] for item in Cluster.query.with_entities(Cluster.name)]
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
