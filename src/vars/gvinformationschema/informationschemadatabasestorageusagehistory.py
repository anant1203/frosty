from .informationschema import InformationSchema

class DatabaseStorageUsageHistoryColumnList:
    _fn=InformationSchema._database_storage_usage_history_fn
    _usage_date="USAGE_DATE"
    _database_id="DATABASE_ID"
    _database_name="DATABASE_NAME"
    _deleted="DELETED"
    _average_database_bytes="AVERAGE_DATABASE_BYTES"
    _average_failsafe_bytes="AVERAGE_FAILSAFE_BYTES"

class InformationSchemaDatabaseStorageUsageHistory:
    def __init__(self):
        self.columns=DatabaseStorageUsageHistoryColumnList()
