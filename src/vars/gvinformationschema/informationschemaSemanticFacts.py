from .informationschema import InformationSchema

class SemanticFactsColumnList:
    _view=InformationSchema._semantic_facts_view
    _semantic_view_catalog="SEMANTIC_VIEW_CATALOG"
    _semantic_view_schema="SEMANTIC_VIEW_SCHEMA"
    _semantic_view_name="SEMANTIC_VIEW_NAME"
    _table_name="TABLE_NAME"
    _fact_name="FACT_NAME"
    _data_type="DATA_TYPE"
    _expr="EXPR"
    _synonyms="SYNONYMS"
    _comment="COMMENT"

class InformationSchemaSemanticFacts:
    def __init__(self):
        self.columns=SemanticFactsColumnList()
