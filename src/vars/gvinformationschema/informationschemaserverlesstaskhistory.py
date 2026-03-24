from .informationschema import InformationSchema

class ServerlessTaskHistoryColumnList:
    _fn=InformationSchema._serverless_task_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _task_name="TASK_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _credits_used="CREDITS_USED"

class InformationSchemaServerlessTaskHistory:
    def __init__(self):
        self.columns=ServerlessTaskHistoryColumnList()
