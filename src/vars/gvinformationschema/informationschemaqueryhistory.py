from .informationschema import InformationSchema

class QueryHistoryColumnList:
    _fn=InformationSchema._query_history_fn
    _query_id="QUERY_ID"
    _query_text="QUERY_TEXT"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _query_type="QUERY_TYPE"
    _session_id="SESSION_ID"
    _user_name="USER_NAME"
    _role_name="ROLE_NAME"
    _warehouse_name="WAREHOUSE_NAME"
    _warehouse_size="WAREHOUSE_SIZE"
    _cluster_number="CLUSTER_NUMBER"
    _query_tag="QUERY_TAG"
    _execution_status="EXECUTION_STATUS"
    _error_code="ERROR_CODE"
    _error_message="ERROR_MESSAGE"
    _start_time="START_TIME"
    _end_time="END_TIME"
    _total_elapsed_time="TOTAL_ELAPSED_TIME"
    _bytes_scanned="BYTES_SCANNED"
    _rows_produced="ROWS_PRODUCED"
    _compilation_time="COMPILATION_TIME"
    _execution_time="EXECUTION_TIME"
    _credits_used_cloud_services="CREDITS_USED_CLOUD_SERVICES"

class InformationSchemaQueryHistory:
    def __init__(self):
        self.columns=QueryHistoryColumnList()
