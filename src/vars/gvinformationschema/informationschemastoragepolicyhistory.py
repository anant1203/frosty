from .informationschema import InformationSchema

class StorageLifecyclePolicyHistoryColumnList:
    _fn=InformationSchema._storage_lifecycle_policy_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _policy_name="POLICY_NAME"
    _database_name="DATABASE_NAME"
    _table_name="TABLE_NAME"
    _schema_name="SCHEMA_NAME"
    _state="STATE"
    _bytes_deleted="BYTES_DELETED"
    _credits_used="CREDITS_USED"

class InformationSchemaStorageLifecyclePolicyHistory:
    def __init__(self):
        self.columns=StorageLifecyclePolicyHistoryColumnList()
