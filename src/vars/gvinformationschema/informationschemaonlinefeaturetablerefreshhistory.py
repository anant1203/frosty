from .informationschema import InformationSchema

class OnlineFeatureTableRefreshHistoryColumnList:
    _fn=InformationSchema._online_feature_table_refresh_history_fn
    _table_name="TABLE_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _refresh_start_time="REFRESH_START_TIME"
    _refresh_end_time="REFRESH_END_TIME"
    _state="STATE"

class InformationSchemaOnlineFeatureTableRefreshHistory:
    def __init__(self):
        self.columns=OnlineFeatureTableRefreshHistoryColumnList()
