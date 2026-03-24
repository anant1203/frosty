from .informationschema import InformationSchema
class StageColumnList:
    _view = InformationSchema._stage_view
    _stage_catalog="STAGE_CATALOG"
    _stage_schema="STAGE_SCHEMA"
    _stage_name="STAGE_NAME"
    _stage_url="STAGE_URL"
    _stage_region="STAGE_REGION"
    _stage_type="STAGE_TYPE"
    _stage_owner="STAGE_OWNER"
    _comment="COMMENT"
    _created="CREATED"
    _last_altered="LAST_ALTERED"

class InformationSchemaStage:
    def __init__(self):
        self.columns=StageColumnList()