from .informationschema import InformationSchema

class SemanticTablesColumnList:
    _view=InformationSchema._semantic_tables_view
    _semantic_view_catalog="SEMANTIC_VIEW_CATALOG"
    _semantic_view_schema="SEMANTIC_VIEW_SCHEMA"
    _semantic_view_name="SEMANTIC_VIEW_NAME"
    _table_name="TABLE_NAME"
    _logical_table_name="LOGICAL_TABLE_NAME"
    _base_table_catalog="BASE_TABLE_CATALOG"
    _base_table_schema="BASE_TABLE_SCHEMA"
    _base_table_name="BASE_TABLE_NAME"

class InformationSchemaSemanticTables:
    def __init__(self):
        self.columns=SemanticTablesColumnList()
