from .informationschema import InformationSchema

class WarehouseMeteringHistoryColumnList:
    _fn=InformationSchema._warehouse_metering_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _entity_id="ENTITY_ID"
    _entity_name="ENTITY_NAME"
    _entity_type="ENTITY_TYPE"
    _granularity="GRANULARITY"
    _credits_used="CREDITS_USED"
    _credits_used_compute="CREDITS_USED_COMPUTE"
    _credits_used_cloud_services="CREDITS_USED_CLOUD_SERVICES"

class InformationSchemaWarehouseMeteringHistory:
    def __init__(self):
        self.columns=WarehouseMeteringHistoryColumnList()
