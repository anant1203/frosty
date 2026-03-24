from .accountusage import AccountUsage

class RolesColumnList:
    _view = f"{AccountUsage._account_usage}.ROLES"
    _created_on = "CREATED_ON"
    _deleted_on = "DELETED_ON"
    _name = "NAME"
    _comment = "COMMENT"
    _owner = "OWNER"

class AccountUsageRoles:
    def __init__(self):
        self.columns = RolesColumnList()
