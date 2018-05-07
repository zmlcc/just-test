from flask import current_app
import kubernetes.client as k8s

from kubernetes.client.rest import ApiException

def create_namespace(cli, name):
    print("create_namespace", name)
    api = k8s.CoreV1Api(cli)
    meta = k8s.V1ObjectMeta(name=name)
    body = k8s.V1Namespace(metadata=meta)
    try:
        rsp = api.create_namespace(body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None
    
    
def delete_namespace(cli, name):
    print("delete_namespace", name)
    
    api = k8s.CoreV1Api(cli)
    body = k8s.V1DeleteOptions(grace_period_seconds=0)
    try:
        rsp = api.delete_namespace(name=name, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


