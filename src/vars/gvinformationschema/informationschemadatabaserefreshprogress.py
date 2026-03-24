from .informationschema import InformationSchema

class DatabaseRefreshProgressColumnList:
    _fn=InformationSchema._database_refresh_progress_fn
    _phase_name="PHASE_NAME"
    _start_time="START_TIME"
    _end_time="END_TIME"
    _progress="PROGRESS"
    _details="DETAILS"

class InformationSchemaDatabaseRefreshProgress:
    def __init__(self):
        self.columns=DatabaseRefreshProgressColumnList()
