from .informationschema import InformationSchema

class ExternalTableFileRegistrationHistoryColumnList:
    _fn=InformationSchema._external_table_file_registration_history_fn
    _system_created_on="SYSTEM_CREATED_ON"
    _file_name="FILE_NAME"
    _status="STATUS"
    _message_source="MESSAGE_SOURCE"
    _last_error="LAST_ERROR"
    _stage_location="STAGE_LOCATION"

class InformationSchemaExternalTableFileRegistrationHistory:
    def __init__(self):
        self.columns=ExternalTableFileRegistrationHistoryColumnList()
