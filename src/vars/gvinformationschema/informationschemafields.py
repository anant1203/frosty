from .informationschema import InformationSchema

class FieldsColumnList:
    _view=InformationSchema._fields_view
    _object_catalog="OBJECT_CATALOG"
    _object_schema="OBJECT_SCHEMA"
    _object_name="OBJECT_NAME"
    _field_path="FIELD_PATH"
    _ordinal_position="ORDINAL_POSITION"
    _data_type="DATA_TYPE"

class InformationSchemaFields:
    def __init__(self):
        self.columns=FieldsColumnList()
