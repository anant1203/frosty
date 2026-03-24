from .informationschema import InformationSchema

class CortexSearchServiceScoringProfilesColumnList:
    _view=InformationSchema._cortex_search_service_scoring_profiles_view
    _service_catalog="SERVICE_CATALOG"
    _service_schema="SERVICE_SCHEMA"
    _service_name="SERVICE_NAME"
    _profile_name="PROFILE_NAME"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaCortexSearchServiceScoringProfiles:
    def __init__(self):
        self.columns=CortexSearchServiceScoringProfilesColumnList()
