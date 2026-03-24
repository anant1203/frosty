from .informationschema import InformationSchema

class WarehouseLoadHistoryColumnList:
    _fn=InformationSchema._warehouse_load_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _warehouse_id="WAREHOUSE_ID"
    _warehouse_name="WAREHOUSE_NAME"
    _avg_running="AVG_RUNNING"
    _avg_queued_load="AVG_QUEUED_LOAD"
    _avg_queued_provisioning="AVG_QUEUED_PROVISIONING"
    _avg_blocked="AVG_BLOCKED"

class InformationSchemaWarehouseLoadHistory:
    def __init__(self):
        self.columns=WarehouseLoadHistoryColumnList()
