from .accountusage import AccountUsage

class TaskHistoryColumnList:
    _view = AccountUsage._task_history_view
    _query_id = "QUERY_ID"
    _name = "NAME"
    _database_name = "DATABASE_NAME"
    _schema_name = "SCHEMA_NAME"
    _query_text = "QUERY_TEXT"
    _condition_text = "CONDITION_TEXT"
    _state = "STATE"
    _error_code = "ERROR_CODE"
    _error_message = "ERROR_MESSAGE"
    _scheduled_time = "SCHEDULED_TIME"
    _query_start_time = "QUERY_START_TIME"
    _next_scheduled_time = "NEXT_SCHEDULED_TIME"
    _completed_time = "COMPLETED_TIME"
    _root_task_id = "ROOT_TASK_ID"
    _graph_version = "GRAPH_VERSION"
    _run_id = "RUN_ID"
    _return_value = "RETURN_VALUE"
    _scheduled_from = "SCHEDULED_FROM"
    _instance_id = "INSTANCE_ID"

class AccountUsageTaskHistory:
    def __init__(self):
        self.columns = TaskHistoryColumnList()
