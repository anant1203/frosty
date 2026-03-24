from .informationschema import InformationSchema

class ElementTypesColumnList:
    _view=InformationSchema._element_types_view
    _object_catalog="OBJECT_CATALOG"
    _object_schema="OBJECT_SCHEMA"
    _object_name="OBJECT_NAME"
    _collection_type_identifier="COLLECTION_TYPE_IDENTIFIER"
    _data_type="DATA_TYPE"

class InformationSchemaElementTypes:
    def __init__(self):
        self.columns=ElementTypesColumnList()
