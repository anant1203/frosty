from .informationschema import InformationSchema

class ReplicationGroupsColumnList:
    _view=InformationSchema._replication_groups_view
    _replication_group_id="REPLICATION_GROUP_ID"
    _replication_group_name="REPLICATION_GROUP_NAME"
    _type="TYPE"
    _is_primary="IS_PRIMARY"
    _is_snapshot="IS_SNAPSHOT"
    _primary="PRIMARY"
    _replication_allowed_to_accounts="REPLICATION_ALLOWED_TO_ACCOUNTS"
    _failover_allowed_to_accounts="FAILOVER_ALLOWED_TO_ACCOUNTS"
    _object_types="OBJECT_TYPES"
    _secondary_state="SECONDARY_STATE"
    _created_on="CREATED_ON"
    _next_scheduled_refresh="NEXT_SCHEDULED_REFRESH"
    _schedule="SCHEDULE"
    _comment="COMMENT"

class InformationSchemaReplicationGroups:
    def __init__(self):
        self.columns=ReplicationGroupsColumnList()
