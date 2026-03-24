from .accountusage import AccountUsage

class WarehouseMeteringHistoryColumnList:
    _view = AccountUsage._warehouse_metering_history_view
    _start_time = "START_TIME"
    _end_time = "END_TIME"
    _warehouse_id = "WAREHOUSE_ID"
    _warehouse_name = "WAREHOUSE_NAME"
    _credits_used = "CREDITS_USED"
    _credits_used_compute = "CREDITS_USED_COMPUTE"
    _credits_used_cloud_services = "CREDITS_USED_CLOUD_SERVICES"

class AccountUsageWarehouseMeteringHistory:
    def __init__(self):
        self.columns = WarehouseMeteringHistoryColumnList()
