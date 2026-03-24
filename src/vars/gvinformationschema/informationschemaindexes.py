from .informationschema import InformationSchema

class IndexesColumnList:
    _view=InformationSchema._indexes_view
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _index_name="INDEX_NAME"
    _index_type="INDEX_TYPE"
    _index_columns="INDEX_COLUMNS"
    _created="CREATED"
    _comment="COMMENT"

class InformationSchemaIndexes:
    def __init__(self):
        self.columns=IndexesColumnList()
