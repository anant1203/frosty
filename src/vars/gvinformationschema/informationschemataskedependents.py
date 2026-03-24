from .informationschema import InformationSchema

class TaskDependentsColumnList:
    _fn=InformationSchema._task_dependents_fn
    _created_on="CREATED_ON"
    _name="NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _owner="OWNER"
    _definition="DEFINITION"
    _warehouse="WAREHOUSE"
    _schedule="SCHEDULE"
    _predecessors="PREDECESSORS"
    _state="STATE"
    _condition="CONDITION"
    _allow_overlapping_execution="ALLOW_OVERLAPPING_EXECUTION"

class InformationSchemaTaskDependents:
    def __init__(self):
        self.columns=TaskDependentsColumnList()
