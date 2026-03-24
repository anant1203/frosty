from .informationschema import InformationSchema

class ApplicationConfigurationsColumnList:
    _view=InformationSchema._application_configurations_view
    _application_name="APPLICATION_NAME"
    _application_owner="APPLICATION_OWNER"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaApplicationConfigurations:
    def __init__(self):
        self.columns=ApplicationConfigurationsColumnList()
