from .informationschema import InformationSchema

class LoginHistoryColumnList:
    _fn=InformationSchema._login_history_fn
    _event_timestamp="EVENT_TIMESTAMP"
    _event_type="EVENT_TYPE"
    _user_name="USER_NAME"
    _client_ip="CLIENT_IP"
    _reported_client_type="REPORTED_CLIENT_TYPE"
    _reported_client_version="REPORTED_CLIENT_VERSION"
    _first_authentication_factor="FIRST_AUTHENTICATION_FACTOR"
    _second_authentication_factor="SECOND_AUTHENTICATION_FACTOR"
    _is_success="IS_SUCCESS"
    _error_code="ERROR_CODE"
    _error_message="ERROR_MESSAGE"

class InformationSchemaLoginHistory:
    def __init__(self):
        self.columns=LoginHistoryColumnList()
