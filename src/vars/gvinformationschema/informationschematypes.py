from .informationschema import InformationSchema

class TypesColumnList:
    _view=InformationSchema._types_view
    _type_catalog="TYPE_CATALOG"
    _type_schema="TYPE_SCHEMA"
    _type_name="TYPE_NAME"
    _type_owner="TYPE_OWNER"
    _data_type="DATA_TYPE"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaTypes:
    def __init__(self):
        self.columns=TypesColumnList()
