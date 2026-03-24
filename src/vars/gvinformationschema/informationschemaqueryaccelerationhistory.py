from .informationschema import InformationSchema

class QueryAccelerationHistoryColumnList:
    _fn=InformationSchema._query_acceleration_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _credits_used="CREDITS_USED"
    _warehouse_name="WAREHOUSE_NAME"
    _warehouse_id="WAREHOUSE_ID"
    _num_files_scanned="NUM_FILES_SCANNED"
    _num_bytes_scanned="NUM_BYTES_SCANNED"

class InformationSchemaQueryAccelerationHistory:
    def __init__(self):
        self.columns=QueryAccelerationHistoryColumnList()
