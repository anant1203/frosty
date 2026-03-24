from .accountusage import AccountUsage

class DataTransferHistoryColumnList:
    _view = f"{AccountUsage._account_usage}.DATA_TRANSFER_HISTORY"
    _start_time = "START_TIME"
    _end_time = "END_TIME"
    _source_cloud = "SOURCE_CLOUD"
    _source_region = "SOURCE_REGION"
    _target_cloud = "TARGET_CLOUD"
    _target_region = "TARGET_REGION"
    _bytes_transferred = "BYTES_TRANSFERRED"
    _transfer_type = "TRANSFER_TYPE"

class AccountUsageDataTransferHistory:
    def __init__(self):
        self.columns = DataTransferHistoryColumnList()
