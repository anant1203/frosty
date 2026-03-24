from .informationschema import InformationSchema

class DynamicTableGraphHistoryColumnList:
    _fn=InformationSchema._dynamic_table_graph_history_fn
    _name="NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _schema_id="SCHEMA_ID"
    _data_timestamp="DATA_TIMESTAMP"

class InformationSchemaDynamicTableGraphHistory:
    def __init__(self):
        self.columns=DynamicTableGraphHistoryColumnList()
