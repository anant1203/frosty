from .accountusage import AccountUsage

class MeteringDailyHistoryColumnList:
    _view = f"{AccountUsage._account_usage}.METERING_DAILY_HISTORY"
    _usage_date = "USAGE_DATE"
    _credits_used_compute = "CREDITS_USED_COMPUTE"
    _credits_used_cloud_services = "CREDITS_USED_CLOUD_SERVICES"
    _credits_used = "CREDITS_USED"
    _credits_adjustment_cloud_services = "CREDITS_ADJUSTMENT_CLOUD_SERVICES"
    _credits_billed = "CREDITS_BILLED"
    _service_type = "SERVICE_TYPE"
    _name = "NAME"

class AccountUsageMeteringDailyHistory:
    def __init__(self):
        self.columns = MeteringDailyHistoryColumnList()
