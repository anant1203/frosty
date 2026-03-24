from .accountusage import AccountUsage

class UsersColumnList:
    _view = AccountUsage._users_view
    _name = "NAME"
    _created_on = "CREATED_ON"
    _deleted_on = "DELETED_ON"
    _login_name = "LOGIN_NAME"
    _display_name = "DISPLAY_NAME"
    _first_name = "FIRST_NAME"
    _last_name = "LAST_NAME"
    _email = "EMAIL"
    _org_identity = "ORG_IDENTITY"
    _comment = "COMMENT"
    _disabled = "DISABLED"
    _must_change_password = "MUST_CHANGE_PASSWORD"
    _snowflake_lock = "SNOWFLAKE_LOCK"
    _default_warehouse = "DEFAULT_WAREHOUSE"
    _default_namespace = "DEFAULT_NAMESPACE"
    _default_role = "DEFAULT_ROLE"
    _ext_authn_duo = "EXT_AUTHN_DUO"
    _ext_authn_uid = "EXT_AUTHN_UID"
    _bypass_mfa_until = "BYPASS_MFA_UNTIL"
    _last_success_login = "LAST_SUCCESS_LOGIN"
    _expires_at_time = "EXPIRES_AT_TIME"
    _locked_until_time = "LOCKED_UNTIL_TIME"
    _has_password = "HAS_PASSWORD"
    _has_rsa_public_key = "HAS_RSA_PUBLIC_KEY"
    _password_last_set_time = "PASSWORD_LAST_SET_TIME"
    _owner = "OWNER"

class AccountUsageUsers:
    def __init__(self):
        self.columns = UsersColumnList()
