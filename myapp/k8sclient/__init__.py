from kubernetes.client.configuration import Configuration
from kubernetes.client.api_client import ApiClient

import os
import atexit
import tempfile
import base64

from ..model import db, Cluster

_client_cache = dict()

_temp_files = {}


def _cleanup_temp_files():
    global _temp_files
    for temp_file in _temp_files.values():
        try:
            os.remove(temp_file)
        except OSError:
            pass
    _temp_files = {}


def _create_temp_file_with_content(content):
    global _temp_files
    if len(_temp_files) == 0:
        atexit.register(_cleanup_temp_files)
    # Because we may change context several times, try to remember files we
    # created and reuse them at a small memory cost.
    content_key = str(content)
    if content_key in _temp_files:
        return _temp_files[content_key]
    _, name = tempfile.mkstemp()
    _temp_files[content_key] = name
    with open(name, 'wb') as fd:
        fd.write(content.encode() if isinstance(content, str) else content)
    return name


def get_cli(cluster_name):
    global _client_cache
    if cluster_name in _client_cache:
        return _client_cache[cluster_name]

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if cluster is None:
        return None

    cfg = Configuration()
    cfg.host = cluster.addr
    cfg.ssl_ca_cert = _create_temp_file_with_content(
        base64.decodestring(cluster.cert))
    cfg.api_key['authorization'] = "Bearer {}".format(cluster.access_token)

    api = ApiClient(cfg)
    _client_cache[cluster_name] = api
    return api


def clean_cli():
    global _client_cache
    _client_cache = dict()
