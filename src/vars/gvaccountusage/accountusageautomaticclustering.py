from .accountusage import AccountUsage

class AutomaticClusteringHistoryColumnList:
    _view = f"{AccountUsage._account_usage}.AUTOMATIC_CLUSTERING_HISTORY"
    _start_time = "START_TIME"
    _end_time = "END_TIME"
    _credits_used = "CREDITS_USED"
    _num_bytes_reclustered = "NUM_BYTES_RECLUSTERED"
    _num_rows_reclustered = "NUM_ROWS_RECLUSTERED"
    _table_id = "TABLE_ID"
    _table_name = "TABLE_NAME"
    _schema_id = "SCHEMA_ID"
    _schema_name = "SCHEMA_NAME"
    _database_id = "DATABASE_ID"
    _database_name = "DATABASE_NAME"

class AccountUsageAutomaticClusteringHistory:
    def __init__(self):
        self.columns = AutomaticClusteringHistoryColumnList()
