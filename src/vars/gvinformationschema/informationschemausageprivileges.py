from .informationschema import InformationSchema

class UsagePrivilegesColumnList:
    _view=InformationSchema._usage_privileges_view
    _grantor="GRANTOR"
    _grantee="GRANTEE"
    _object_catalog="OBJECT_CATALOG"
    _object_schema="OBJECT_SCHEMA"
    _object_name="OBJECT_NAME"
    _object_type="OBJECT_TYPE"
    _privilege_type="PRIVILEGE_TYPE"
    _is_grantable="IS_GRANTABLE"

class InformationSchemaUsagePrivileges:
    def __init__(self):
        self.columns=UsagePrivilegesColumnList()
