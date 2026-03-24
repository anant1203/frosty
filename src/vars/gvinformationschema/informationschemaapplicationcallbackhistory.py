from .informationschema import InformationSchema

class ApplicationCallbackHistoryColumnList:
    _fn=InformationSchema._application_callback_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _application_name="APPLICATION_NAME"
    _callback_type="CALLBACK_TYPE"
    _status="STATUS"

class InformationSchemaApplicationCallbackHistory:
    def __init__(self):
        self.columns=ApplicationCallbackHistoryColumnList()
