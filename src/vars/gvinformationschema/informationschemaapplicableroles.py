from .informationschema import InformationSchema

class ApplicableRolesColumnList:
    _view=InformationSchema._applicable_roles_view
    _grantee="GRANTEE"
    _role_name="ROLE_NAME"
    _role_owner="ROLE_OWNER"
    _is_grantable="IS_GRANTABLE"

class InformationSchemaApplicableRoles:
    def __init__(self):
        self.columns=ApplicableRolesColumnList()
