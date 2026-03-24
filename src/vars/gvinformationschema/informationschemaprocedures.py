from .informationschema import InformationSchema

class ProceduresColumnList:
    _view=InformationSchema._procedures_view
    _procedure_catalog="PROCEDURE_CATALOG"
    _procedure_schema="PROCEDURE_SCHEMA"
    _procedure_name="PROCEDURE_NAME"
    _procedure_owner="PROCEDURE_OWNER"
    _argument_signature="ARGUMENT_SIGNATURE"
    _data_type="DATA_TYPE"
    _procedure_definition="PROCEDURE_DEFINITION"
    _procedure_language="PROCEDURE_LANGUAGE"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaProcedures:
    def __init__(self):
        self.columns=ProceduresColumnList()
