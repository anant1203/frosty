from .informationschema import InformationSchema

class ReferentialConstraintsColumnList:
    _view=InformationSchema._referential_constraints_view
    _constraint_catalog="CONSTRAINT_CATALOG"
    _constraint_schema="CONSTRAINT_SCHEMA"
    _constraint_name="CONSTRAINT_NAME"
    _unique_constraint_catalog="UNIQUE_CONSTRAINT_CATALOG"
    _unique_constraint_schema="UNIQUE_CONSTRAINT_SCHEMA"
    _unique_constraint_name="UNIQUE_CONSTRAINT_NAME"
    _match_option="MATCH_OPTION"
    _update_rule="UPDATE_RULE"
    _delete_rule="DELETE_RULE"

class InformationSchemaReferentialConstraints:
    def __init__(self):
        self.columns=ReferentialConstraintsColumnList()
