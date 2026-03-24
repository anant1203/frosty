from .informationschema import InformationSchema

class CurrentTaskGraphsColumnList:
    _fn=InformationSchema._current_task_graphs_fn
    _root_task_name="ROOT_TASK_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _state="STATE"
    _first_error_task_name="FIRST_ERROR_TASK_NAME"
    _first_error_code="FIRST_ERROR_CODE"
    _first_error_message="FIRST_ERROR_MESSAGE"
    _scheduled_from="SCHEDULED_FROM"
    _scheduled_time="SCHEDULED_TIME"
    _query_start_time="QUERY_START_TIME"
    _next_scheduled_time="NEXT_SCHEDULED_TIME"
    _completed_time="COMPLETED_TIME"
    _task_graph_run_group_id="TASK_GRAPH_RUN_GROUP_ID"
    _graph_version="GRAPH_VERSION"
    _run_id="RUN_ID"
    _return_value="RETURN_VALUE"

class InformationSchemaCurrentTaskGraphs:
    def __init__(self):
        self.columns=CurrentTaskGraphsColumnList()
