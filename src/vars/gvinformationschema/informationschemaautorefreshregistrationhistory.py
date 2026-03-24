from .informationschema import InformationSchema

class AutoRefreshRegistrationHistoryColumnList:
    _fn=InformationSchema._auto_refresh_registration_history_fn
    _created_on="CREATED_ON"
    _stage_location="STAGE_LOCATION"
    _entity_name="ENTITY_NAME"
    _entity_type="ENTITY_TYPE"
    _file_name="FILE_NAME"
    _status="STATUS"
    _error_message="ERROR_MESSAGE"

class InformationSchemaAutoRefreshRegistrationHistory:
    def __init__(self):
        self.columns=AutoRefreshRegistrationHistoryColumnList()
