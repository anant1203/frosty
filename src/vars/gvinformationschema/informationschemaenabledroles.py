from .informationschema import InformationSchema

class EnabledRolesColumnList:
    _view=InformationSchema._enabled_roles_view
    _role_name="ROLE_NAME"

class InformationSchemaEnabledRoles:
    def __init__(self):
        self.columns=EnabledRolesColumnList()
