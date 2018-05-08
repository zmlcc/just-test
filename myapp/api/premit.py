from flask import jsonify, request, g, current_app
from . import api

from ..model import db, Cluster, Namespace, User, Project, Account

from cerberus import Validator
from sqlalchemy.orm import load_only
from sqlalchemy import exc

from .. import k8sclient as k8s


@api.route("/cluster/<cluster_name>/permit/<ns_name>", methods=["POST"])
def create_permit(cluster_name, ns_name):
    pass



def get_


def do_rb():
    pass


def bind_ns(account, ns):
    account.namespace  = ns
    try:
        db.session().commit()
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)
        return None
    
    return True