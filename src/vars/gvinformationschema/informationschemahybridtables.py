from .informationschema import InformationSchema

class HybridTablesColumnList:
    _view=InformationSchema._hybrid_tables_view
    _table_catalog="CATALOG"
    _table_schema="SCHEMA"
    _table_name="NAME"
    _table_owner="OWNER"
    _row_count="ROW_COUNT"
    _bytes="BYTES"
    _retention_time="RETENTION_TIME"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaHybridTables:
    def __init__(self):
        self.columns=HybridTablesColumnList()
