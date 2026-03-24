from .informationschema import InformationSchema

class SearchOptimizationHistoryColumnList:
    _fn=InformationSchema._search_optimization_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _table_name="TABLE_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _credits_used="CREDITS_USED"
    _bytes_added="BYTES_ADDED"
    _bytes_deleted="BYTES_DELETED"
    _table_id="TABLE_ID"

class InformationSchemaSearchOptimizationHistory:
    def __init__(self):
        self.columns=SearchOptimizationHistoryColumnList()
