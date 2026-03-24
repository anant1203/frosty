from .informationschema import InformationSchema

class MaterializedViewRefreshHistoryColumnList:
    _fn=InformationSchema._materialized_view_refresh_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _table_name="TABLE_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _credits_used="CREDITS_USED"
    _bytes_credited="BYTES_CREDITED"
    _table_id="TABLE_ID"

class InformationSchemaMaterializedViewRefreshHistory:
    def __init__(self):
        self.columns=MaterializedViewRefreshHistoryColumnList()
