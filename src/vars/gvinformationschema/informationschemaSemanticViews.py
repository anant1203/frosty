from .informationschema import InformationSchema

class SemanticViewsColumnList:
    _view=InformationSchema._semantic_views_view
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _table_owner="TABLE_OWNER"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaSemanticViews:
    def __init__(self):
        self.columns=SemanticViewsColumnList()
