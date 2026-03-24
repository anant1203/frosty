from .informationschema import InformationSchema

class DynamicTableRefreshHistoryColumnList:
    _fn=InformationSchema._dynamic_table_refresh_history_fn
    _name="NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _state="STATE"
    _state_code="STATE_CODE"
    _state_message="STATE_MESSAGE"
    _query_id="QUERY_ID"
    _data_timestamp="DATA_TIMESTAMP"
    _refresh_start_time="REFRESH_START_TIME"
    _refresh_end_time="REFRESH_END_TIME"
    _completion_target="COMPLETION_TARGET"
    _qualified_name="QUALIFIED_NAME"

class InformationSchemaDynamicTableRefreshHistory:
    def __init__(self):
        self.columns=DynamicTableRefreshHistoryColumnList()
