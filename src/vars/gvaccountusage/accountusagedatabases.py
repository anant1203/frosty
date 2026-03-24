from .accountusage import AccountUsage

class DatabasesColumnList:
    _view = f"{AccountUsage._account_usage}.DATABASES"
    _database_id = "DATABASE_ID"
    _database_name = "DATABASE_NAME"
    _database_owner = "DATABASE_OWNER"
    _is_transient = "IS_TRANSIENT"
    _retention_time = "RETENTION_TIME"
    _created = "CREATED"
    _last_altered = "LAST_ALTERED"
    _deleted = "DELETED"
    _comment = "COMMENT"
    _type = "TYPE"

class AccountUsageDatabases:
    def __init__(self):
        self.columns = DatabasesColumnList()
