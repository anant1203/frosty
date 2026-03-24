from .informationschema import InformationSchema

class SemanticRelationshipsColumnList:
    _view=InformationSchema._semantic_relationships_view
    _semantic_view_catalog="SEMANTIC_VIEW_CATALOG"
    _semantic_view_schema="SEMANTIC_VIEW_SCHEMA"
    _semantic_view_name="SEMANTIC_VIEW_NAME"
    _left_table="LEFT_TABLE"
    _right_table="RIGHT_TABLE"
    _left_join_key="LEFT_JOIN_KEY"
    _right_join_key="RIGHT_JOIN_KEY"
    _relationship_type="RELATIONSHIP_TYPE"

class InformationSchemaSemanticRelationships:
    def __init__(self):
        self.columns=SemanticRelationshipsColumnList()
