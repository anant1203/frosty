from .informationschema import InformationSchema

class ApplicationSpecificationsColumnList:
    _view=InformationSchema._application_specifications_view
    _application_name="APPLICATION_NAME"
    _specification_name="SPECIFICATION_NAME"
    _created="CREATED"
    _last_altered="LAST_ALTERED"

class InformationSchemaApplicationSpecifications:
    def __init__(self):
        self.columns=ApplicationSpecificationsColumnList()
