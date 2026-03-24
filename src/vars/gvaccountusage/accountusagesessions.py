from .accountusage import AccountUsage

class SessionsColumnList:
    _view = f"{AccountUsage._account_usage}.SESSIONS"
    _session_id = "SESSION_ID"
    _created_on = "CREATED_ON"
    _user_name = "USER_NAME"
    _authentication_method = "AUTHENTICATION_METHOD"
    _login_event_id = "LOGIN_EVENT_ID"
    _client_application_id = "CLIENT_APPLICATION_ID"
    _client_application = "CLIENT_APPLICATION"
    _client_environment = "CLIENT_ENVIRONMENT"
    _client_build_id = "CLIENT_BUILD_ID"
    _client_version = "CLIENT_VERSION"

class AccountUsageSessions:
    def __init__(self):
        self.columns = SessionsColumnList()
