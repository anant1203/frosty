from .informationschema import InformationSchema

class SemanticMetricsColumnList:
    _view=InformationSchema._semantic_metrics_view
    _semantic_view_catalog="SEMANTIC_VIEW_CATALOG"
    _semantic_view_schema="SEMANTIC_VIEW_SCHEMA"
    _semantic_view_name="SEMANTIC_VIEW_NAME"
    _metric_name="METRIC_NAME"
    _data_type="DATA_TYPE"
    _expr="EXPR"
    _synonyms="SYNONYMS"
    _comment="COMMENT"

class InformationSchemaSemanticMetrics:
    def __init__(self):
        self.columns=SemanticMetricsColumnList()
