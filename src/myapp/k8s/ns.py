from flask import current_app
import kubernetes.client as k8c

from kubernetes.client.rest import ApiException

def create_namespace(cli, name):
    current_app.logger.debug("create_namespace:", name)
    
    api = k8c.CoreV1Api(cli)
    meta = k8c.V1ObjectMeta(name=name)
    body = k8c.V1Namespace(metadata=meta)
    try:
        rsp = api.create_namespace(body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None
    
    
def delete_namespace(cli, name):
    current_app.logger.debug("delete_namespace:", name)
    
    api = k8c.CoreV1Api(cli)
    body = k8c.V1DeleteOptions(grace_period_seconds=0)
    try:
        rsp = api.delete_namespace(name=name, body=body)
        return rsp
    except ApiException as e:
        current_app.logger.error(e)
        return None


