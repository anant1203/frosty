from .accountusage import AccountUsage

class AlertHistoryColumnList:
    _view = f"{AccountUsage._account_usage}.ALERT_HISTORY"
    _name = "NAME"
    _database_name = "DATABASE_NAME"
    _schema_name = "SCHEMA_NAME"
    _condition = "CONDITION"
    _condition_query_id = "CONDITION_QUERY_ID"
    _action = "ACTION"
    _action_query_id = "ACTION_QUERY_ID"
    _state = "STATE"
    _error_code = "ERROR_CODE"
    _error_message = "ERROR_MESSAGE"
    _scheduled_time = "SCHEDULED_TIME"
    _completed_time = "COMPLETED_TIME"

class AccountUsageAlertHistory:
    def __init__(self):
        self.columns = AlertHistoryColumnList()
