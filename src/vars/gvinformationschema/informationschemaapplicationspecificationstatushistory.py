from .informationschema import InformationSchema

class ApplicationSpecificationStatusHistoryColumnList:
    _fn=InformationSchema._application_specification_status_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _application_name="APPLICATION_NAME"
    _specification_name="SPECIFICATION_NAME"
    _status="STATUS"

class InformationSchemaApplicationSpecificationStatusHistory:
    def __init__(self):
        self.columns=ApplicationSpecificationStatusHistoryColumnList()
