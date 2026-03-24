from .informationschema import InformationSchema

class ReplicationGroupRefreshProgressColumnList:
    _fn=InformationSchema._replication_group_refresh_progress_fn
    _phase_name="PHASE_NAME"
    _start_time="START_TIME"
    _end_time="END_TIME"
    _progress="PROGRESS"
    _details="DETAILS"

class InformationSchemaReplicationGroupRefreshProgress:
    def __init__(self):
        self.columns=ReplicationGroupRefreshProgressColumnList()
