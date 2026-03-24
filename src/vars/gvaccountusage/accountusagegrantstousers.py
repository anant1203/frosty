from .accountusage import AccountUsage

class GrantsToUsersColumnList:
    _view = f"{AccountUsage._account_usage}.GRANTS_TO_USERS"
    _created_on = "CREATED_ON"
    _deleted_on = "DELETED_ON"
    _role = "ROLE"
    _granted_to = "GRANTED_TO"
    _grantee_name = "GRANTEE_NAME"
    _granted_by = "GRANTED_BY"

class AccountUsageGrantsToUsers:
    def __init__(self):
        self.columns = GrantsToUsersColumnList()
