from .informationschema import InformationSchema

class DynamicTablesColumnList:
    _fn=InformationSchema._dynamic_tables_fn
    _refresh_mode="REFRESH_MODE"
    _name="NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _text="TEXT"
    _cluster_by="CLUSTER_BY"
    _warehouse="WAREHOUSE"
    _scheduling_state="SCHEDULING_STATE"
    _data_timestamp="DATA_TIMESTAMP"
    _last_suspended_on="LAST_SUSPENDED_ON"
    _rows="ROWS"
    _bytes="BYTES"
    _target_lag="TARGET_LAG"
    _refresh_mode_reason="REFRESH_MODE_REASON"
    _automatic_clustering="AUTOMATIC_CLUSTERING"
    _scheduling_state_reason="SCHEDULING_STATE_REASON"
    _owner="OWNER"
    _owner_role_type="OWNER_ROLE_TYPE"
    _created_on="CREATED_ON"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaDynamicTables:
    def __init__(self):
        self.columns=DynamicTablesColumnList()
