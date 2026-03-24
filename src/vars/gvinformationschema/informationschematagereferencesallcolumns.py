from .informationschema import InformationSchema

class TagReferencesAllColumnsColumnList:
    _fn=InformationSchema._tag_references_all_columns_fn
    _tag_database="TAG_DATABASE"
    _tag_schema="TAG_SCHEMA"
    _tag_name="TAG_NAME"
    _tag_value="TAG_VALUE"
    _object_database="OBJECT_DATABASE"
    _object_schema="OBJECT_SCHEMA"
    _object_name="OBJECT_NAME"
    _object_id="OBJECT_ID"
    _column_name="COLUMN_NAME"
    _tag_level="TAG_LEVEL"
    _domain="DOMAIN"

class InformationSchemaTagReferencesAllColumns:
    def __init__(self):
        self.columns=TagReferencesAllColumnsColumnList()
