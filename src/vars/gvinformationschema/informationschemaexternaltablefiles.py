from .informationschema import InformationSchema

class ExternalTableFilesColumnList:
    _fn=InformationSchema._external_table_files_fn
    _file_name="FILE_NAME"
    _registered_on="REGISTERED_ON"
    _file_size="FILE_SIZE"
    _status="STATUS"
    _last_error="LAST_ERROR"

class InformationSchemaExternalTableFiles:
    def __init__(self):
        self.columns=ExternalTableFilesColumnList()
