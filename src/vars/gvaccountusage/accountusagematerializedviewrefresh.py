from .accountusage import AccountUsage

class MaterializedViewRefreshHistoryColumnList:
    _view = f"{AccountUsage._account_usage}.MATERIALIZED_VIEW_REFRESH_HISTORY"
    _start_time = "START_TIME"
    _end_time = "END_TIME"
    _credits_used = "CREDITS_USED"
    _num_bytes_maintained = "NUM_BYTES_MAINTAINED"
    _num_rows_maintained = "NUM_ROWS_MAINTAINED"
    _table_id = "TABLE_ID"
    _table_name = "TABLE_NAME"
    _schema_id = "SCHEMA_ID"
    _schema_name = "SCHEMA_NAME"
    _database_id = "DATABASE_ID"
    _database_name = "DATABASE_NAME"

class AccountUsageMaterializedViewRefreshHistory:
    def __init__(self):
        self.columns = MaterializedViewRefreshHistoryColumnList()
