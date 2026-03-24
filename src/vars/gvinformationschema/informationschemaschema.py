from .informationschema import InformationSchema
class SchemaColumnList:
    _view = InformationSchema._schema_view
    catalog_name = "CATALOG_NAME"
    schema_name = "SCHEMA_NAME"
    schema_owner = "SCHEMA_OWNER"
    is_transient = "IS_TRANSIENT"
    is_managed_access = "IS_MANAGED_ACCESS"
    retention_time = "RETENTION_TIME"
    default_character_set_catalog = "DEFAULT_CHARACTER_SET_CATALOG"
    default_character_set_schema = "DEFAULT_CHARACTER_SET_SCHEMA"
    default_character_set_name = "DEFAULT_CHARACTER_SET_NAME"
    sql_path = "SQL_PATH"
    created = "CREATED"
    last_altered = "LAST_ALTERED"
    comment = "COMMENT"



class InformationSchemaSchema:
    def __init__(self):
        self.columns = SchemaColumnList()
