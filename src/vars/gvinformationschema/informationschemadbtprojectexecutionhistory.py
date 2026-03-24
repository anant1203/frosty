from .informationschema import InformationSchema

class DbtProjectExecutionHistoryColumnList:
    _fn=InformationSchema._dbt_project_execution_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _project_name="PROJECT_NAME"
    _status="STATUS"
    _invocation_id="INVOCATION_ID"

class InformationSchemaDbtProjectExecutionHistory:
    def __init__(self):
        self.columns=DbtProjectExecutionHistoryColumnList()
