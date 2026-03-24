from .informationschema import InformationSchema

class PolicyReferencesColumnList:
    _fn=InformationSchema._policy_references_fn
    _policy_db="POLICY_DB"
    _policy_schema="POLICY_SCHEMA"
    _policy_name="POLICY_NAME"
    _policy_kind="POLICY_KIND"
    _ref_database_name="REF_DATABASE_NAME"
    _ref_schema_name="REF_SCHEMA_NAME"
    _ref_entity_name="REF_ENTITY_NAME"
    _ref_entity_domain="REF_ENTITY_DOMAIN"
    _ref_column_name="REF_COLUMN_NAME"
    _ref_arg_column_names="REF_ARG_COLUMN_NAMES"
    _policy_status="POLICY_STATUS"
    _created="CREATED"
    _last_modified="LAST_MODIFIED"

class InformationSchemaPolicyReferences:
    def __init__(self):
        self.columns=PolicyReferencesColumnList()
