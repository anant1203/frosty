from .informationschema import InformationSchema

class ModelVersionsColumnList:
    _view=InformationSchema._model_versions_view
    _model_catalog="MODEL_CATALOG"
    _model_schema="MODEL_SCHEMA"
    _model_name="MODEL_NAME"
    _model_owner="MODEL_OWNER"
    _version_name="VERSION_NAME"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaModelVersions:
    def __init__(self):
        self.columns=ModelVersionsColumnList()
