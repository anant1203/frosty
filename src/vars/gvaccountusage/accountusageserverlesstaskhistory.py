from .accountusage import AccountUsage

class ServerlessTaskHistoryColumnList:
    _view = f"{AccountUsage._account_usage}.SERVERLESS_TASK_HISTORY"
    _start_time = "START_TIME"
    _end_time = "END_TIME"
    _task_id = "TASK_ID"
    _task_name = "TASK_NAME"
    _credits_used = "CREDITS_USED"
    _schema_id = "SCHEMA_ID"
    _schema_name = "SCHEMA_NAME"
    _database_id = "DATABASE_ID"
    _database_name = "DATABASE_NAME"

class AccountUsageServerlessTaskHistory:
    def __init__(self):
        self.columns = ServerlessTaskHistoryColumnList()
