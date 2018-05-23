import time
from flask import jsonify, request, g, current_app
from . import api

from ..model import db, Cluster, Namespace, User, Project, Account

from cerberus import Validator
from sqlalchemy.orm import load_only
from sqlalchemy import exc

from .. import k8s
from .util import get_sa_name


@api.route("/cluster/<cluster_name>/account", methods=["GET"])
def get_cluster_account(cluster_name):
    if g.cur_user is None:
        return "", 400

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    acc = Account.query.filter(Account.user == g.cur_user).filter(
        Account.cluster == cluster).first()

    if acc is None:
        return "", 204

    output = dict(cluster=cluster_name, user=g.cur_user.name, token=acc.token)

    return jsonify(output)


@api.route("/cluster/<cluster_name>/account", methods=["POST"])
def create_cluster_account(cluster_name):
    if g.cur_user is None:
        return "", 400

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    cli = k8s.get_cli(cluster_name)
    if cli is None:
        return "", 400

    sa_name = get_sa_name(g.cur_user.name)

    create_acc = create_account

    create_acc = read_account_wrapper(cli, sa_name)(create_acc)
    create_acc = create_account_wrapper(cli, sa_name)(create_acc)
    rsp = create_acc(cluster, g.cur_user)
    if rsp is None:
        return "", 400

    return "", 204


def create_account(cluster, user, token):
    acc = Account()
    acc.cluster = cluster
    acc.user = user
    acc.token = token

    try:
        db.session().add(acc)
        db.session().commit()
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)
        return None

    return True


def create_account_wrapper(cli, sa_name):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            rsp = k8s.create_serviceaccount(cli, sa_name)
            if rsp is None:
                return None

            print(rsp)

            rsp = func(*args, **kwargs)
            if rsp is None:
                k8s.delete_serviceaccount(cli, sa_name)

            return rsp

        return _wrapper

    return wrapper


def read_account_wrapper(cli, sa_name, count=10):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            for _ in range(count):
                rsp = k8s.read_serviceaccount(cli, sa_name)
                if rsp is None:
                    return None

                print(rsp)

                if rsp.secrets:
                    break

                time.sleep(0.2)

            if not rsp.secrets:
                return None

            token_name = rsp.secrets[0].name

            rsp = k8s.read_secret(cli, token_name)

            print(rsp)

            token = rsp.data.get('token', "")

            return func(token=token, *args, **kwargs)

        return _wrapper

    return wrapper
