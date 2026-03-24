from .informationschema import InformationSchema

class ClassInstanceFunctionsColumnList:
    _view=InformationSchema._class_instance_functions_view
    _instance_catalog="INSTANCE_CATALOG"
    _instance_schema="INSTANCE_SCHEMA"
    _instance_name="INSTANCE_NAME"
    _function_name="FUNCTION_NAME"
    _argument_signature="ARGUMENT_SIGNATURE"
    _data_type="DATA_TYPE"

class InformationSchemaClassInstanceFunctions:
    def __init__(self):
        self.columns=ClassInstanceFunctionsColumnList()
