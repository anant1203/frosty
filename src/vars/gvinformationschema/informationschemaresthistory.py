from .informationschema import InformationSchema

class RestEventHistoryColumnList:
    _fn=InformationSchema._rest_event_history_fn
    _event_timestamp="EVENT_TIMESTAMP"
    _event_id="EVENT_ID"
    _event_type="EVENT_TYPE"
    _endpoint="ENDPOINT"
    _method="METHOD"
    _status="STATUS"
    _error_code="ERROR_CODE"
    _client_ip="CLIENT_IP"
    _actor_name="ACTOR_NAME"
    _resource_name="RESOURCE_NAME"
    _details="DETAILS"

class InformationSchemaRestEventHistory:
    def __init__(self):
        self.columns=RestEventHistoryColumnList()
