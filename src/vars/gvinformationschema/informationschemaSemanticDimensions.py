from .informationschema import InformationSchema

class SemanticDimensionsColumnList:
    _view=InformationSchema._semantic_dimensions_view
    _semantic_view_catalog="SEMANTIC_VIEW_CATALOG"
    _semantic_view_schema="SEMANTIC_VIEW_SCHEMA"
    _semantic_view_name="SEMANTIC_VIEW_NAME"
    _table_name="TABLE_NAME"
    _dimension_name="DIMENSION_NAME"
    _data_type="DATA_TYPE"
    _expr="EXPR"
    _synonyms="SYNONYMS"
    _comment="COMMENT"

class InformationSchemaSemanticDimensions:
    def __init__(self):
        self.columns=SemanticDimensionsColumnList()
