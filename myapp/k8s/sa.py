from flask import current_app
import kubernetes.client as k8c

from kubernetes.client.rest import ApiException

from . import DEFAULT_SA_NAMESPACE


def create_serviceaccount(cli, name, ns=DEFAULT_SA_NAMESPACE):
    print("create_serviceaccount", name)
    
    api = k8c.CoreV1Api(cli)
    meta = k8c.V1ObjectMeta(name=name)
    body = k8c.V1ServiceAccount(metadata=meta)
    try:
        rsp = api.create_namespaced_service_account(namespace=ns, body=body)
        api.list_namespaced_service_account
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


def delete_serviceaccount(cli, name, ns=DEFAULT_SA_NAMESPACE):
    print("delete_serviceaccount", name)

    api = k8c.CoreV1Api(cli)
    body = k8c.V1DeleteOptions(grace_period_seconds=0)
    try:
        rsp = api.delete_namespaced_service_account(
            name=name, namespace=ns, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None



def read_serviceaccount(cli, name, ns=DEFAULT_SA_NAMESPACE):
    print('read_serviceaccount')

    api = k8c.CoreV1Api(cli)
    
    try:
        rsp = api.read_namespaced_service_account(name=name, namespace=ns)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None

def read_secret(cli, name, ns=DEFAULT_SA_NAMESPACE):
    print('read_secret')

    api = k8c.CoreV1Api(cli)
    
    try:
        rsp = api.read_namespaced_secret(name=name, namespace=ns)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None
