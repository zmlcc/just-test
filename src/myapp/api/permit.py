from flask import jsonify, g, current_app
from sqlalchemy import exc
from . import api

from ..model import db, Cluster, Namespace, Project, Account


from .. import k8s

from .util import get_sa_name, get_rb_name


@api.route("/cluster/<cluster_name>/permit/<ns_name>", methods=["POST"])
def create_permit(cluster_name, ns_name):
    if g.cur_user is None:
        return "", 400

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    acc = Account.query.filter(Account.user == g.cur_user).filter(
        Account.cluster == cluster).first()
    if acc is None:
        return "", 400

    prj = Project.query.filter(Project.user.contains(
        g.cur_user)).filter(Project.name == ns_name).first()
    if prj is None:
        return "", 400

    ns = Namespace.query.filter(Namespace.cluster == cluster).filter(
        Namespace.project == prj).first()
    if ns is None:
        return "", 400

    cli = k8s.get_cli(cluster_name)
    if cli is None:
        return "", 400

    sa_name = get_sa_name(g.cur_user.name)

    create_permit_action = bind_ns_indb
    create_permit_action = create_sa_rb_wrapper(cli, ns_name,
                                                sa_name)(create_permit_action)

    rsp = create_permit_action(acc, ns)
    if rsp is None:
        return "", 400

    return "", 204


@api.route("/cluster/<cluster_name>/permit", methods=["GET"])
def get_all_permit(cluster_name):
    if g.cur_user is None:
        return "", 400

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return "", 400

    acc = Account.query.filter(Account.user == g.cur_user).filter(
        Account.cluster == cluster).first()
    if acc is None:
        return "", 400

    ns = Namespace.query.filter(Namespace.cluster == cluster).filter(
        Namespace.account.contains(acc))

    output = []

    for item in ns:
        output.append(dict(namespace=item.project.name))

    return jsonify(output)


def create_sa_rb_wrapper(cli, ns, sa_name):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            sa_ns = current_app.config.get("UAE_SA_NS", "")
            if sa_ns is "":
                return None
            role_name = current_app.config.get("UAE_BASE_CR", "")
            if role_name is "":
                return None
            role_kind = "ClusterRole"
            rb_name = get_rb_name(role_name, sa_name)
            rsp = k8s.create_sa_rb(cli, ns, rb_name, role_name, role_kind,
                                   sa_name, sa_ns)
            if rsp is None:
                return None

            current_app.logger.debug("create_sa_rb:", rsp)

            rsp = func(*args, **kwargs)
            if rsp is None:
                # k8s.de
                pass

            return rsp

        return _wrapper

    return wrapper


def bind_ns_indb(account, ns):
    account.namespace.append(ns)
    try:
        db.session.commit()    # pylint: disable=e1101
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)
        return None

    return True
