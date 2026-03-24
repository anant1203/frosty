from .informationschema import InformationSchema

class ServerlessAlertHistoryColumnList:
    _fn=InformationSchema._serverless_alert_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _name="NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _credits_used="CREDITS_USED"

class InformationSchemaServerlessAlertHistory:
    def __init__(self):
        self.columns=ServerlessAlertHistoryColumnList()
