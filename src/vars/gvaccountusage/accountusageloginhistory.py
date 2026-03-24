from .accountusage import AccountUsage

class LoginHistoryColumnList:
    _view = AccountUsage._login_history_view
    _event_id = "EVENT_ID"
    _event_timestamp = "EVENT_TIMESTAMP"
    _event_type = "EVENT_TYPE"
    _user_name = "USER_NAME"
    _client_ip = "CLIENT_IP"
    _reported_client_type = "REPORTED_CLIENT_TYPE"
    _reported_client_version = "REPORTED_CLIENT_VERSION"
    _first_authentication_factor = "FIRST_AUTHENTICATION_FACTOR"
    _second_authentication_factor = "SECOND_AUTHENTICATION_FACTOR"
    _is_success = "IS_SUCCESS"
    _error_code = "ERROR_CODE"
    _error_message = "ERROR_MESSAGE"
    _related_event_id = "RELATED_EVENT_ID"
    _connection = "CONNECTION"

class AccountUsageLoginHistory:
    def __init__(self):
        self.columns = LoginHistoryColumnList()
