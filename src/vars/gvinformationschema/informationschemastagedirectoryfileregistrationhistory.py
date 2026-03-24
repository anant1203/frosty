from .informationschema import InformationSchema

class StageDirectoryFileRegistrationHistoryColumnList:
    _fn=InformationSchema._stage_directory_file_registration_history_fn
    _system_created_on="SYSTEM_CREATED_ON"
    _file_name="FILE_NAME"
    _status="STATUS"
    _message_source="MESSAGE_SOURCE"
    _last_error="LAST_ERROR"

class InformationSchemaStageDirectoryFileRegistrationHistory:
    def __init__(self):
        self.columns=StageDirectoryFileRegistrationHistoryColumnList()
