from .informationschema import InformationSchema

class TableColumnList:
    _view = InformationSchema._table_view
    _table_catalog = "TABLE_CATALOG"
    _table_schema = "TABLE_SCHEMA"
    _table_name = "TABLE_NAME"
    _table_owner = "TABLE_OWNER"
    _table_type = "TABLE_TYPE"
    _is_transient = "IS_TRANSIENT"
    _clustering_key = "CLUSTERING_KEY"
    _row_count = "ROW_COUNT"
    _bytes = "BYTES"
    _retention_time = "RETENTION_TIME"
    _created = "CREATED"
    _last_altered = "LAST_ALTERED"
    _last_ddl = "LAST_DDL"
    _last_ddl_by = "LAST_DDL_BY"
    _auto_clustering_on = "AUTO_CLUSTERING_ON"
    _comment = "COMMENT"
    _is_temporary = "IS_TEMPORARY"
    _is_iceberg = "IS_ICEBERG"
    _is_dynamic="IS_DYNAMIC"
    _is_mutable="IS_IMMUTABLE"

class InformationSchemaTable:
    def __init__(self):
        self.columns=TableColumnList()
