from .informationschema import InformationSchema

class AutomaticClusteringHistoryColumnList:
    _fn=InformationSchema._automatic_clustering_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _table_name="TABLE_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _credits_used="CREDITS_USED"
    _num_bytes_reclustered="NUM_BYTES_RECLUSTERED"
    _num_rows_reclustered="NUM_ROWS_RECLUSTERED"
    _table_id="TABLE_ID"

class InformationSchemaAutomaticClusteringHistory:
    def __init__(self):
        self.columns=AutomaticClusteringHistoryColumnList()
