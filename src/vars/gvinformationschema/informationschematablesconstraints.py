from .informationschema import InformationSchema

class TableConstraintsColumnList:
    _view=InformationSchema._table_constraints_view
    _constraint_catalog="CONSTRAINT_CATALOG"
    _constraint_schema="CONSTRAINT_SCHEMA"
    _constraint_name="CONSTRAINT_NAME"
    _table_catalog="TABLE_CATALOG"
    _table_schema="TABLE_SCHEMA"
    _table_name="TABLE_NAME"
    _constraint_type="CONSTRAINT_TYPE"
    _is_deferrable="IS_DEFERRABLE"
    _initially_deferred="INITIALLY_DEFERRED"
    _enforced="ENFORCED"
    _rely="RELY"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaTableConstraints:
    def __init__(self):
        self.columns=TableConstraintsColumnList()
