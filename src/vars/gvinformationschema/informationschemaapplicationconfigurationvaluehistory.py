from .informationschema import InformationSchema

class ApplicationConfigurationValueHistoryColumnList:
    _fn=InformationSchema._application_configuration_value_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _application_name="APPLICATION_NAME"
    _key="KEY"
    _value="VALUE"

class InformationSchemaApplicationConfigurationValueHistory:
    def __init__(self):
        self.columns=ApplicationConfigurationValueHistoryColumnList()
