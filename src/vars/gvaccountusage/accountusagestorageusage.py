from .accountusage import AccountUsage

class StorageUsageColumnList:
    _view = AccountUsage._storage_usage_view
    _usage_date = "USAGE_DATE"
    _average_database_bytes = "AVERAGE_DATABASE_BYTES"
    _average_failsafe_bytes = "AVERAGE_FAILSAFE_BYTES"
    _average_stage_bytes = "AVERAGE_STAGE_BYTES"

class AccountUsageStorageUsage:
    def __init__(self):
        self.columns = StorageUsageColumnList()
