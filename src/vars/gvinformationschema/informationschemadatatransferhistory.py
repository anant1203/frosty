from .informationschema import InformationSchema

class DataTransferHistoryColumnList:
    _fn=InformationSchema._data_transfer_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _source_cloud="SOURCE_CLOUD"
    _source_region="SOURCE_REGION"
    _target_cloud="TARGET_CLOUD"
    _target_region="TARGET_REGION"
    _bytes_transferred="BYTES_TRANSFERRED"
    _transfer_type="TRANSFER_TYPE"

class InformationSchemaDataTransferHistory:
    def __init__(self):
        self.columns=DataTransferHistoryColumnList()
