from flask import current_app
import kubernetes.client as k8c

from kubernetes.client.rest import ApiException


def create_role(cli, namespace, role):
    current_app.logger.debug("create_role:", namespace, role)
    api = k8c.RbacAuthorizationV1Api(cli)
    try:
        rsp = api.create_namespaced_role(namespace=namespace, body=role)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


def delete_role(cli, namespace, name):
    current_app.logger.debug("delete_role:", namespace, name)
    

    api = k8c.RbacAuthorizationV1Api(cli)
    body = k8c.V1DeleteOptions(grace_period_seconds=0)
    try:
        rsp = api.delete_namespaced_role(
            name=name, namespace=namespace, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


def create_role_binding(cli, namespace, name, role, subject):
    current_app.logger.debug("create_role_binding:", namespace, name, role, subject)
    
    api = k8c.RbacAuthorizationV1Api(cli)
    meta = k8c.V1ObjectMeta(name=name)
    body = k8c.V1RoleBinding(metadata=meta, role_ref=role, subjects=subject)
    try:
        rsp = api.create_namespaced_role_binding(namespace=namespace, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


def create_sa_rb(cli,
                 namespace,
                 name,
                 role_name,
                 role_kind,
                 sa_name,
                 sa_ns):
    role = k8c.V1RoleRef(
        name=role_name, api_group="rbac.authorization.k8s.io", kind=role_kind)
    subject = [
        k8c.V1Subject(kind="ServiceAccount", name=sa_name, namespace=sa_ns)
    ]
    return create_role_binding(cli, namespace, name, role, subject)
