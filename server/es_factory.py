from datetime import datetime

from elasticsearch import Elasticsearch, Transport

from config import config

log = config.logger(__file__)

_instances = {}


class MissingClusterConfiguration(Exception):
    """
    Exception when cluster configuration is not found in config files
    """
    pass


class InvalidClusterConfiguration(Exception):
    """
    Exception when cluster configuration does not contain required properties
    """
    pass


def connect(cluster_name):
    """
    Returns the es client for the cluster.
    Connects to the cluster if did not connect previously
    :param cluster_name: Dot separated cluster path in the configuration file
    :return: es client
    :raises MissingClusterConfiguration: in case no config section is found for the cluster
    :raises InvalidClusterConfiguration: in case cluster config section misses needed properties
    """
    if cluster_name not in _instances:
        cluster_config = _get_cluster_config(cluster_name)
        hosts = cluster_config.get('hosts', None)
        if not hosts:
            raise InvalidClusterConfiguration(cluster_name)
        args = cluster_config.get('args', {})
        _instances[cluster_name] = Elasticsearch(hosts=hosts, transport_class=Transport, **args)

    return _instances[cluster_name]


def _get_cluster_config(cluster_name):
    """
    Returns cluster config for the specified cluster path
    :param cluster_name: Dot separated cluster path in the configuration file
    :return: config section for the cluster
    :raises MissingClusterConfiguration: in case no config section is found for the cluster
    """
    cluster_key = '.'.join(('hosts.elastic', cluster_name))
    cluster_config = config.get(cluster_key, None)
    if not cluster_config:
        raise MissingClusterConfiguration(cluster_name)

    return cluster_config


def connect_all():
    clusters = config.get("hosts.elastic").as_plain_ordered_dict()
    for name in clusters:
        connect(name)


def instances():
    return _instances


def timestamp_str_to_millis(ts_str):
    epoch = datetime.utcfromtimestamp(0)
    current_date = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int((current_date - epoch).total_seconds() * 1000.0)


def get_timestamp_millis():
    now = datetime.utcnow()
    epoch = datetime.utcfromtimestamp(0)
    return int((now - epoch).total_seconds() * 1000.0)


def get_es_timestamp_str():
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (now.microsecond / 1000) + "Z"
