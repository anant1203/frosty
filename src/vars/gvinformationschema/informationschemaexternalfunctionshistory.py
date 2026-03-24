from .informationschema import InformationSchema

class ExternalFunctionsHistoryColumnList:
    _fn=InformationSchema._external_functions_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _function_name="FUNCTION_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _invocations="INVOCATIONS"
    _sent_rows="SENT_ROWS"
    _received_rows="RECEIVED_ROWS"
    _sent_bytes="SENT_BYTES"
    _received_bytes="RECEIVED_BYTES"

class InformationSchemaExternalFunctionsHistory:
    def __init__(self):
        self.columns=ExternalFunctionsHistoryColumnList()
