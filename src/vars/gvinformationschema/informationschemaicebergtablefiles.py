from .informationschema import InformationSchema

class IcebergTableFilesColumnList:
    _fn=InformationSchema._iceberg_table_files_fn
    _file_name="FILE_NAME"
    _file_size="FILE_SIZE"
    _registered_on="REGISTERED_ON"
    _status="STATUS"
    _last_error="LAST_ERROR"

class InformationSchemaIcebergTableFiles:
    def __init__(self):
        self.columns=IcebergTableFilesColumnList()
