from .accountusage import AccountUsage

class GrantsToRolesColumnList:
    _view = AccountUsage._grants_to_roles_view
    _created_on = "CREATED_ON"
    _modified_on = "MODIFIED_ON"
    _privilege = "PRIVILEGE"
    _granted_on = "GRANTED_ON"
    _name = "NAME"
    _table_catalog = "TABLE_CATALOG"
    _table_schema = "TABLE_SCHEMA"
    _granted_to = "GRANTED_TO"
    _grantee_name = "GRANTEE_NAME"
    _grant_option = "GRANT_OPTION"
    _granted_by = "GRANTED_BY"
    _deleted_on = "DELETED_ON"
    _granted_by_role_type = "GRANTED_BY_ROLE_TYPE"

class AccountUsageGrantsToRoles:
    def __init__(self):
        self.columns = GrantsToRolesColumnList()
