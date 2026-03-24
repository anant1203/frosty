from .accountusage import AccountUsage

class PipesColumnList:
    _view = f"{AccountUsage._account_usage}.PIPES"
    _pipe_id = "PIPE_ID"
    _pipe_name = "PIPE_NAME"
    _pipe_schema_id = "PIPE_SCHEMA_ID"
    _pipe_schema = "PIPE_SCHEMA"
    _pipe_catalog_id = "PIPE_CATALOG_ID"
    _pipe_catalog = "PIPE_CATALOG"
    _is_autoingest_enabled = "IS_AUTOINGEST_ENABLED"
    _definition = "DEFINITION"
    _created = "CREATED"
    _last_altered = "LAST_ALTERED"
    _deleted = "DELETED"
    _comment = "COMMENT"
    _owner = "OWNER"
    _notification_channel_name = "NOTIFICATION_CHANNEL_NAME"

class AccountUsagePipes:
    def __init__(self):
        self.columns = PipesColumnList()
