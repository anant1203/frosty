from .informationschema import InformationSchema

class TaskHistoryColumnList:
    _fn=InformationSchema._task_history_fn
    _query_id="QUERY_ID"
    _query_text="QUERY_TEXT"
    _name="NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _scheduled_time="SCHEDULED_TIME"
    _query_start_time="QUERY_START_TIME"
    _next_scheduled_time="NEXT_SCHEDULED_TIME"
    _completed_time="COMPLETED_TIME"
    _state="STATE"
    _return_value="RETURN_VALUE"
    _error_code="ERROR_CODE"
    _error_message="ERROR_MESSAGE"

class InformationSchemaTaskHistory:
    def __init__(self):
        self.columns=TaskHistoryColumnList()
