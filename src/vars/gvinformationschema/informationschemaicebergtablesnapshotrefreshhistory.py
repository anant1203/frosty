from .informationschema import InformationSchema

class IcebergTableSnapshotRefreshHistoryColumnList:
    _fn=InformationSchema._iceberg_table_snapshot_refresh_history_fn
    _table_name="TABLE_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _snapshot_id="SNAPSHOT_ID"
    _refresh_mode="REFRESH_MODE"
    _refresh_start_time="REFRESH_START_TIME"
    _refresh_end_time="REFRESH_END_TIME"
    _state="STATE"

class InformationSchemaIcebergTableSnapshotRefreshHistory:
    def __init__(self):
        self.columns=IcebergTableSnapshotRefreshHistoryColumnList()
