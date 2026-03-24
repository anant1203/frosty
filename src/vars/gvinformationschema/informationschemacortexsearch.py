from .informationschema import InformationSchema

class CortexSearchColumnList:
    _view = InformationSchema._cortex_search_view
    _service_catalog = "SERVICE_CATALOG"
    _service_schema = "SERVICE_SCHEMA"
    _service_name = "SERVICE_NAME"
    _created = "CREATED"
    _definition = "DEFINITION"
    _search_column = "SEARCH_COLUMN"
    _attribute_columns = "ATTRIBUTE_COLUMNS"
    _columns = "COLUMNS"
    _target_lag = "TARGET_LAG"
    _warehouse = "WAREHOUSE"
    _comment = "COMMENT"
    _service_query_url = "SERVICE_QUERY_URL"
    _owner = "OWNER"
    _owner_role_type = "OWNER_ROLE_TYPE"
    _data_fresh_as_of = "DATA_FRESH_AS_OF"
    _data_timestamp = "DATA_TIMESTAMP"
    _source_data_bytes = "SOURCE_DATA_BYTES"
    _source_data_num_rows = "SOURCE_DATA_NUM_ROWS"
    _indexing_state = "INDEXING_STATE"
    _indexing_error = "INDEXING_ERROR"
    _serving_state = "SERVING_STATE"
    _serving_data_bytes = "SERVING_DATA_BYTES"
    _embedding_model = "EMBEDDING_MODEL"

class InformationSchemaCortexSearch:
    def __init__(self):
        self.columns = CortexSearchColumnList()
