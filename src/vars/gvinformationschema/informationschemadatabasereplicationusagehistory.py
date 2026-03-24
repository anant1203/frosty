from .informationschema import InformationSchema

class DatabaseReplicationUsageHistoryColumnList:
    _fn=InformationSchema._database_replication_usage_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _database_name="DATABASE_NAME"
    _database_id="DATABASE_ID"
    _credits_used="CREDITS_USED"
    _bytes_transferred="BYTES_TRANSFERRED"

class InformationSchemaDatabaseReplicationUsageHistory:
    def __init__(self):
        self.columns=DatabaseReplicationUsageHistoryColumnList()
