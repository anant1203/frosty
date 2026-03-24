from .informationschema import InformationSchema

class ClassInstanceProceduresColumnList:
    _view=InformationSchema._class_instance_procedures_view
    _instance_catalog="INSTANCE_CATALOG"
    _instance_schema="INSTANCE_SCHEMA"
    _instance_name="INSTANCE_NAME"
    _procedure_name="PROCEDURE_NAME"
    _argument_signature="ARGUMENT_SIGNATURE"
    _data_type="DATA_TYPE"

class InformationSchemaClassInstanceProcedures:
    def __init__(self):
        self.columns=ClassInstanceProceduresColumnList()
