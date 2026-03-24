from .informationschema import InformationSchema

class DatabaseColumnList:
    _view = InformationSchema._database_view
    database_name = "DATABASE_NAME"
    database_owner = "DATABASE_OWNER"
    is_transient = "IS_TRANSIENT"
    comment = "COMMENT"
    created = "CREATED"
    last_altered = "LAST_ALTERED"
    retention_time = "RETENTION_TIME"
    type = "TYPE"
    owner_role_type = "OWNER_ROLE_TYPE"


class InformationSchemaDatabase:
    def __init__(self):
        self.columns = DatabaseColumnList()
