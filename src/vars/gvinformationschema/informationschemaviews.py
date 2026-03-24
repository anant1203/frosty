from .informationschema import InformationSchema

class ViewsColumnList:
    _view=InformationSchema._views_view
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _view_definition="VIEW_DEFINITION"
    _check_option="CHECK_OPTION"
    _is_updatable="IS_UPDATABLE"
    _insertable_into="INSERTABLE_INTO"
    _is_secure="IS_SECURE"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _last_ddl="LAST_DDL"
    _last_ddl_by="LAST_DDL_BY"
    _comment="COMMENT"

class InformationSchemaViews:
    def __init__(self):
        self.columns=ViewsColumnList()
