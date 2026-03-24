from .informationschema import InformationSchema

class AlertHistoryColumnList:
    _fn=InformationSchema._alert_history_fn
    _name="NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _scheduled_time="SCHEDULED_TIME"
    _query_start_time="QUERY_START_TIME"
    _completed_time="COMPLETED_TIME"
    _state="STATE"
    _error_code="ERROR_CODE"
    _error_message="ERROR_MESSAGE"
    _query_id="QUERY_ID"

class InformationSchemaAlertHistory:
    def __init__(self):
        self.columns=AlertHistoryColumnList()
