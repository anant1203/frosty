from .informationschema import InformationSchema
class PipeColumnList:
    _view=InformationSchema._pipe_view
    _pipe_catalog="PIPE_CATALOG"
    _pipe_schema="PIPE_SCHEMA"
    _pipe_name="PIPE_NAME"
    _pipe_owner="PIPE_OWNER"
    _definition="DEFINITION"
    _is_autoingest_enabled="IS_AUTOINGEST_ENABLED"
    _notification_channel_name="NOTIFICATION_CHANNEL_NAME"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"
    _pattern="PATTERN"

class InformationSchemaPipe:
    def __init__(self):
        self.columns=PipeColumnList()