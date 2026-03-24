from .accountusage import AccountUsage

class WarehouseEventsHistoryColumnList:
    _view = f"{AccountUsage._account_usage}.WAREHOUSE_EVENTS_HISTORY"
    _timestamp = "TIMESTAMP"
    _warehouse_id = "WAREHOUSE_ID"
    _warehouse_name = "WAREHOUSE_NAME"
    _cluster_number = "CLUSTER_NUMBER"
    _event_name = "EVENT_NAME"
    _event_reason = "EVENT_REASON"
    _event_state = "EVENT_STATE"
    _user_name = "USER_NAME"
    _role_name = "ROLE_NAME"
    _query_id = "QUERY_ID"

class AccountUsageWarehouseEventsHistory:
    def __init__(self):
        self.columns = WarehouseEventsHistoryColumnList()
