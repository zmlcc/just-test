from flask import current_app
import kubernetes.client as k8s

from kubernetes.client.rest import ApiException

from . import DEFAULT_SA_NAMESPACE


def create_role(cli, namespace, name, rule):
    print("create_role", name)
    api = k8s.RbacAuthorizationV1Api(cli)
    meta = k8s.V1ObjectMeta(name=name)
    body = k8s.V1Role(metadata=meta, rules=rule)

    try:
        rsp = api.create_namespaced_role(namespace=namespace, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


def delete_role(cli, namespace, name):
    print("delete_role", name)

    api = k8s.RbacAuthorizationV1Api(cli)
    body = k8s.V1DeleteOptions(grace_period_seconds=0)
    try:
        rsp = api.delete_namespaced_role(
            name=name, namespace=namespace, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


def create_role_binding(cli, namespace, name, role, subject):
    print("create_role_binding", name)
    api = k8s.RbacAuthorizationV1Api(cli)
    meta = k8s.V1ObjectMeta(name=name)
    body = k8s.V1RoleBinding(metadata=meta, role_ref=role, subjects=subject)
    try:
        rsp = api.create_namespaced_role(namespace=namespace, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


def create_sa_rb(cli,
                 namespace,
                 name,
                 role_name,
                 sa_name,
                 sa_ns=DEFAULT_SA_NAMESPACE):
    role = k8s.V1RoleRef(
        name=role_name, api_group="rbac.authorization.k8s.io", kind="Role")
    subject = [
        k8s.V1Subject(kind="ServiceAccount", name=sa_name, namespace=sa_ns)
    ]
    return create_role_binding(cli, namespace, name, role, subject)
