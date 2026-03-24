from .informationschema import InformationSchema

class CortexSearchRefreshHistoryColumnList:
    _fn=InformationSchema._cortex_search_refresh_history_fn
    _service_name="SERVICE_NAME"
    _database_name="DATABASE_NAME"
    _schema_name="SCHEMA_NAME"
    _embedding_model="EMBEDDING_MODEL"
    _refresh_start_time="REFRESH_START_TIME"
    _refresh_end_time="REFRESH_END_TIME"
    _state="STATE"
    _credits_used="CREDITS_USED"

class InformationSchemaCortexSearchRefreshHistory:
    def __init__(self):
        self.columns=CortexSearchRefreshHistoryColumnList()
