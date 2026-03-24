from .informationschema import InformationSchema

class ClassInstancesColumnList:
    _view=InformationSchema._class_instances_view
    _instance_catalog="INSTANCE_CATALOG"
    _instance_schema="INSTANCE_SCHEMA"
    _instance_name="INSTANCE_NAME"
    _instance_owner="INSTANCE_OWNER"
    _class_catalog="CLASS_CATALOG"
    _class_schema="CLASS_SCHEMA"
    _class_name="CLASS_NAME"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaClassInstances:
    def __init__(self):
        self.columns=ClassInstancesColumnList()
