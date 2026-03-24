from .informationschema import InformationSchema

class FunctionsColumnList:
    _view=InformationSchema._functions_view
    _function_catalog="FUNCTION_CATALOG"
    _function_schema="FUNCTION_SCHEMA"
    _function_name="FUNCTION_NAME"
    _function_owner="FUNCTION_OWNER"
    _argument_signature="ARGUMENT_SIGNATURE"
    _data_type="DATA_TYPE"
    _function_definition="FUNCTION_DEFINITION"
    _function_language="FUNCTION_LANGUAGE"
    _volatility="VOLATILITY"
    _is_null_call="IS_NULL_CALL"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaFunctions:
    def __init__(self):
        self.columns=FunctionsColumnList()
