from .accountusage import AccountUsage

class StagesColumnList:
    _view = f"{AccountUsage._account_usage}.STAGES"
    _stage_id = "STAGE_ID"
    _stage_name = "STAGE_NAME"
    _stage_schema_id = "STAGE_SCHEMA_ID"
    _stage_schema = "STAGE_SCHEMA"
    _stage_catalog_id = "STAGE_CATALOG_ID"
    _stage_catalog = "STAGE_CATALOG"
    _stage_url = "STAGE_URL"
    _stage_region = "STAGE_REGION"
    _stage_type = "STAGE_TYPE"
    _data_retention_time_in_days = "DATA_RETENTION_TIME_IN_DAYS"
    _created = "CREATED"
    _last_altered = "LAST_ALTERED"
    _deleted = "DELETED"
    _comment = "COMMENT"
    _owner = "OWNER"

class AccountUsageStages:
    def __init__(self):
        self.columns = StagesColumnList()
