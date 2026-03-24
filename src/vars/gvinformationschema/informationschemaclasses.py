from .informationschema import InformationSchema

class ClassesColumnList:
    _view=InformationSchema._classes_view
    _class_catalog="CLASS_CATALOG"
    _class_schema="CLASS_SCHEMA"
    _class_name="CLASS_NAME"
    _class_owner="CLASS_OWNER"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaClasses:
    def __init__(self):
        self.columns=ClassesColumnList()
