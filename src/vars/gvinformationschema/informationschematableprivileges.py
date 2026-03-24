from .informationschema import InformationSchema

class TablePrivilegesColumnList:
    _view=InformationSchema._table_privileges_view
    _grantor="GRANTOR"
    _grantee="GRANTEE"
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _privilege_type="PRIVILEGE_TYPE"
    _is_grantable="IS_GRANTABLE"
    _with_hierarchy="WITH_HIERARCHY"

class InformationSchemaTablePrivileges:
    def __init__(self):
        self.columns=TablePrivilegesColumnList()
