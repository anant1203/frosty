from .informationschema import InformationSchema

class ReplicationGroupUsageHistoryColumnList:
    _fn=InformationSchema._replication_group_usage_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _replication_group_name="REPLICATION_GROUP_NAME"
    _credits_used="CREDITS_USED"
    _bytes_transferred="BYTES_TRANSFERRED"

class InformationSchemaReplicationGroupUsageHistory:
    def __init__(self):
        self.columns=ReplicationGroupUsageHistoryColumnList()
