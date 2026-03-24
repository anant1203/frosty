from .informationschema import InformationSchema

class DataMetricFunctionReferencesColumnList:
    _fn=InformationSchema._data_metric_function_references_fn
    _metric_database_name="METRIC_DATABASE_NAME"
    _metric_schema_name="METRIC_SCHEMA_NAME"
    _metric_name="METRIC_NAME"
    _ref_database_name="REF_DATABASE_NAME"
    _ref_schema_name="REF_SCHEMA_NAME"
    _ref_entity_name="REF_ENTITY_NAME"
    _ref_entity_domain="REF_ENTITY_DOMAIN"
    _ref_column_names="REF_COLUMN_NAMES"
    _schedule="SCHEDULE"
    _schedule_status="SCHEDULE_STATUS"
    _argument_data_types="ARGUMENT_DATA_TYPES"

class InformationSchemaDataMetricFunctionReferences:
    def __init__(self):
        self.columns=DataMetricFunctionReferencesColumnList()
