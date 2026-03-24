from .informationschema import InformationSchema

class StageStorageUsageHistoryColumnList:
    _fn=InformationSchema._stage_storage_usage_history_fn
    _usage_date="USAGE_DATE"
    _average_stage_bytes="AVERAGE_STAGE_BYTES"

class InformationSchemaStageStorageUsageHistory:
    def __init__(self):
        self.columns=StageStorageUsageHistoryColumnList()
