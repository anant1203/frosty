from .informationschema import InformationSchema

class TableStorageMetricsColumnList:
    _view=InformationSchema._table_storage_metrics_view
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _id="ID"
    _clone_group_id="CLONE_GROUP_ID"
    _is_transient="IS_TRANSIENT"
    _active_bytes="ACTIVE_BYTES"
    _time_travel_bytes="TIME_TRAVEL_BYTES"
    _failsafe_bytes="FAILSAFE_BYTES"
    _retained_for_clone_bytes="RETAINED_FOR_CLONE_BYTES"
    _table_created="TABLE_CREATED"
    _table_dropped="TABLE_DROPPED"
    _table_entered_failsafe="TABLE_ENTERED_FAILSAFE"
    _catalog_created="CATALOG_CREATED"
    _catalog_dropped="CATALOG_DROPPED"
    _schema_created="SCHEMA_CREATED"
    _schema_dropped="SCHEMA_DROPPED"
    _comment="COMMENT"

class InformationSchemaTableStorageMetrics:
    def __init__(self):
        self.columns=TableStorageMetricsColumnList()
