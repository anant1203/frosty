from .informationschema import InformationSchema

class ExternalTablesColumnList:
    _view=InformationSchema._external_tables_view
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _table_owner="TABLE_OWNER"
    _table_type="TABLE_TYPE"
    _stage_url="STAGE_URL"
    _location="LOCATION"
    _file_format_type="FILE_FORMAT_TYPE"
    _comment="COMMENT"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _last_ddl="LAST_DDL"
    _last_ddl_by="LAST_DDL_BY"

class InformationSchemaExternalTables:
    def __init__(self):
        self.columns=ExternalTablesColumnList()
