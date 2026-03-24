from .informationschema import InformationSchema

class ReplicationGroupRefreshHistoryColumnList:
    _fn=InformationSchema._replication_group_refresh_history_fn
    _replication_group_name="REPLICATION_GROUP_NAME"
    _start_time="START_TIME"
    _end_time="END_TIME"
    _status="STATUS"
    _credits_used="CREDITS_USED"
    _bytes_transferred="BYTES_TRANSFERRED"

class InformationSchemaReplicationGroupRefreshHistory:
    def __init__(self):
        self.columns=ReplicationGroupRefreshHistoryColumnList()
