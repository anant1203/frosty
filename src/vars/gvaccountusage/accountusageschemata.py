from .accountusage import AccountUsage

class SchemataColumnList:
    _view = f"{AccountUsage._account_usage}.SCHEMATA"
    _schema_id = "SCHEMA_ID"
    _schema_name = "SCHEMA_NAME"
    _schema_owner = "SCHEMA_OWNER"
    _catalog_id = "CATALOG_ID"
    _catalog_name = "CATALOG_NAME"
    _is_transient = "IS_TRANSIENT"
    _retention_time = "RETENTION_TIME"
    _created = "CREATED"
    _last_altered = "LAST_ALTERED"
    _deleted = "DELETED"
    _comment = "COMMENT"

class AccountUsageSchemata:
    def __init__(self):
        self.columns = SchemataColumnList()
