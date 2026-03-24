from .informationschema import InformationSchema

class ReplicationDatabasesColumnList:
    _view=InformationSchema._replication_databases_view
    _database_name="DATABASE_NAME"
    _is_primary="IS_PRIMARY"
    _is_snapshot="IS_SNAPSHOT"
    _primary_database="PRIMARY_DATABASE"
    _primary_database_url="PRIMARY_DATABASE_URL"
    _replication_allowed_to_accounts="REPLICATION_ALLOWED_TO_ACCOUNTS"
    _failover_allowed_to_accounts="FAILOVER_ALLOWED_TO_ACCOUNTS"
    _organization_name="ORGANIZATION_NAME"
    _account_name="ACCOUNT_NAME"
    _snowflake_region="SNOWFLAKE_REGION"
    _created_on="CREATED_ON"
    _comment="COMMENT"

class InformationSchemaReplicationDatabases:
    def __init__(self):
        self.columns=ReplicationDatabasesColumnList()
