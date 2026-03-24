from .informationschema import InformationSchema

class IndexColumnsColumnList:
    _view=InformationSchema._index_columns_view
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _index_name="INDEX_NAME"
    _column_name="COLUMN_NAME"
    _ordinal_position="ORDINAL_POSITION"

class InformationSchemaIndexColumns:
    def __init__(self):
        self.columns=IndexColumnsColumnList()
