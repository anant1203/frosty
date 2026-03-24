from .informationschema import InformationSchema

class DatabaseRefreshHistoryColumnList:
    _fn=InformationSchema._database_refresh_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _source_database_name="SOURCE_DATABASE_NAME"
    _target_database_name="TARGET_DATABASE_NAME"
    _status="STATUS"

class InformationSchemaDatabaseRefreshHistory:
    def __init__(self):
        self.columns=DatabaseRefreshHistoryColumnList()
