from .informationschema import InformationSchema

class ReplicationGroupDanglingReferencesColumnList:
    _fn=InformationSchema._replication_group_dangling_references_fn
    _created_on="CREATED_ON"
    _object_db="OBJECT_DB"
    _object_schema="OBJECT_SCHEMA"
    _object_name="OBJECT_NAME"
    _object_kind="OBJECT_KIND"
    _referencing_db="REFERENCING_DB"
    _referencing_schema="REFERENCING_SCHEMA"
    _referencing_object_name="REFERENCING_OBJECT_NAME"
    _referencing_object_kind="REFERENCING_OBJECT_KIND"
    _reference_type="REFERENCE_TYPE"

class InformationSchemaReplicationGroupDanglingReferences:
    def __init__(self):
        self.columns=ReplicationGroupDanglingReferencesColumnList()
