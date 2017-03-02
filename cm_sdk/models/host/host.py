from cm_sdk.models.common.common import CloudManagerBase, CloudManagerEnum
import cm_sdk.models.host.host

__author__ = 'e0d'


class TypeName(CloudManagerEnum):
    MASTER = "MASTER"
    NO_DATA = "NO_DATA"
    RECOVERING = "RECOVERING"
    REPLICA_ARBITER = "REPLICA_ARBITER"
    REPLICA_PRIMARY = "REPLICA_PRIMARY"
    REPLICA_SECONDARY = "REPLICA_SECONDARY"
    SHARD_CONFIG = "SHARD_CONFIG"
    SHARD_MONGOS = "SHARD_MONGOS"
    SHARD_PRIMARY = "SHARD_PRIMARY"
    SHARD_SECONDARY = "SHARD_SECONDARY"
    SHARD_STANDALONE = "SHARD_STANDALONE"
    SLAVE = "SLAVE"
    STANDALONE = "STANDALONE"


class Host(CloudManagerBase):

    children = {'type_name': {'class': TypeName}}

    my_api_attributes = ['alerts_enabled', 'auth_mechanism_name', 'cluster_id', 'deactivated', 'has_startup_warnings', 'hidden', 'host_enabled', 'hostname', 'ip_address', 'journaling_enabled', 'last_data_size_bytes', 'last_index_size_bytes', 'last_ping', 'logs_enabled', 'low_ulimit', 'munin_enabled', 'port', 'profiler_enabled', 'replica_set_name', 'replica_state_name', 'ssl_enabled', 'type_name', 'uptime_msec', 'username', 'version']

    def __init__(self, alerts_enabled=None, auth_mechanism_name=None, cluster_id=None, deactivated=None, has_startup_warnings=None, hidden=None, host_enabled=None, hostname=None, ip_address=None, journaling_enabled=None, last_data_size_bytes=None, last_index_size_bytes=None, last_ping=None, logs_enabled=None, low_ulimit=None, munin_enabled=None, port=None, profiler_enabled=None, replica_set_name=None, replica_state_name=None, ssl_enabled=None, type_name=None, uptime_msec=None, username=None, version=None):

        CloudManagerBase.__init__(self, self.my_api_attributes)
        self.alerts_enabled = alerts_enabled
        self.auth_mechanism_name = auth_mechanism_name
        self.cluster_id = cluster_id
        self.deactivated = deactivated
        self.has_startup_warnings = has_startup_warnings
        self.hidden = hidden
        self.host_enabled = host_enabled
        self.hostname = hostname
        self.ip_address = ip_address
        self.journaling_enabled = journaling_enabled
        self.last_data_size_bytes = last_data_size_bytes
        self.last_index_size_bytes = last_index_size_bytes
        self.last_ping = last_ping
        self.logs_enabled = logs_enabled
        self.low_ulimit = low_ulimit
        self.munin_enabled = munin_enabled
        self.port = port
        self.profiler_enabled = profiler_enabled
        self.replica_set_name = replica_set_name
        self.replica_state_name = replica_state_name
        self.ssl_enabled = ssl_enabled
        self.type_name = type_name
        self.uptime_msec = uptime_msec
        self.username = username
        self.version = version
