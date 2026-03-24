
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from .baseprivilege import BasePrivilege

from src.validation import ValidateObject as vo

class DatabasePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing DatabasePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='DATABASE')
        vo.database_exist(session=session,database_name=object_identifier)
        super().set_object_identifier(val=object_identifier)

class UserPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing UserPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='USER')
        vo.user_exist(session=session,user_name=object_identifier)
        super().set_object_identifier(val=object_identifier)

class StagePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing StagePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='STAGE')
        vo.stage_exist(session=session,database_name=database,schema_name=schema,stage_name=object_identifier)
        super().set_object_identifier(val=object_identifier)

class WarehousePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing WarehousePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='WAREHOUSE')
        vo.warehouse_exist(session=session,warehouse_name=object_identifier)
        super().set_object_identifier(val=object_identifier)

class SchemaPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database):
        logger.info(f"Initializing SchemaPrivileges for {object_identifier} in {database}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SCHEMA')
        vo.schema_exist(session=session,database_name=database,schema_name=object_identifier)
        super().set_object_identifier(val=object_identifier)

class TablePrivileges(BasePrivilege):
     def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing TablePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='TABLE')
        vo.table_exist(session=session,database_name=database,schema_name=schema,table_name=object_identifier)
        super().set_object_identifier(val=object_identifier)

class FileFormatPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing FileFormatPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='FILEFORMAT')
        vo.file_format_exist(session=session,database_name=database,schema_name=schema,file_format_name=object_identifier)
        super().set_object_identifier(val=object_identifier)

class SnowpipePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing SnowpipePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='PIPE')
        super().set_object_identifier(val=object_identifier)

class StreamPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing StreamPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='STREAM')
        super().set_object_identifier(val=object_identifier)

class TaskPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing TaskPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='TASK')
        super().set_object_identifier(val=object_identifier)

class ResourceMonitorPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ResourceMonitorPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='RESOURCEMONITOR')
        super().set_object_identifier(val=object_identifier)

# Account-level objects

class RolePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing RolePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='ROLE')
        super().set_object_identifier(val=object_identifier)

class ExternalVolumePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ExternalVolumePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='EXTERNALVOLUME')
        super().set_object_identifier(val=object_identifier)

class FailoverGroupPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing FailoverGroupPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='FAILOVERGROUP')
        super().set_object_identifier(val=object_identifier)

class ReplicationGroupPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ReplicationGroupPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='REPLICATIONGROUP')
        super().set_object_identifier(val=object_identifier)

class IntegrationPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing IntegrationPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='INTEGRATION')
        super().set_object_identifier(val=object_identifier)

class NetworkPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing NetworkPolicyPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='NETWORKPOLICY')
        super().set_object_identifier(val=object_identifier)

class DataExchangePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing DataExchangePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='DATAEXCHANGE')
        super().set_object_identifier(val=object_identifier)

class ListingPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ListingPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='LISTING')
        super().set_object_identifier(val=object_identifier)

class OrganizationProfilePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing OrganizationProfilePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='ORGANIZATIONPROFILE')
        super().set_object_identifier(val=object_identifier)

class ConnectionPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ConnectionPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='CONNECTION')
        super().set_object_identifier(val=object_identifier)

class ComputePoolPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ComputePoolPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='COMPUTEPOOL')
        super().set_object_identifier(val=object_identifier)

class ProvisionedThroughputPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ProvisionedThroughputPrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='PROVISIONEDTHROUGHPUT')
        super().set_object_identifier(val=object_identifier)

class ApplicationPackagePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier):
        logger.info(f"Initializing ApplicationPackagePrivileges for {object_identifier}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='APPLICATIONPACKAGE')
        super().set_object_identifier(val=object_identifier)

# Database-level objects

class DatabaseRolePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database):
        logger.info(f"Initializing DatabaseRolePrivileges for {object_identifier} in {database}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='DATABASEROLE')
        super().set_object_identifier(val=object_identifier)

# Schema-level objects

class AuthenticationPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing AuthenticationPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='AUTHENTICATIONPOLICY')
        super().set_object_identifier(val=object_identifier)

class NetworkRulePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing NetworkRulePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='NETWORKRULE')
        super().set_object_identifier(val=object_identifier)

class PackagesPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing PackagesPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='PACKAGESPOLICY')
        super().set_object_identifier(val=object_identifier)

class PasswordPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing PasswordPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='PASSWORDPOLICY')
        super().set_object_identifier(val=object_identifier)

class SessionPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing SessionPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SESSIONPOLICY')
        super().set_object_identifier(val=object_identifier)

class DynamicTablePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing DynamicTablePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='DYNAMICTABLE')
        super().set_object_identifier(val=object_identifier)

class EventTablePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing EventTablePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='EVENTTABLE')
        super().set_object_identifier(val=object_identifier)

class ExternalTablePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ExternalTablePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='EXTERNALTABLE')
        super().set_object_identifier(val=object_identifier)

class HybridTablePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing HybridTablePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='HYBRIDTABLE')
        super().set_object_identifier(val=object_identifier)

class IcebergTablePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing IcebergTablePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='ICEBERGTABLE')
        super().set_object_identifier(val=object_identifier)

class ViewPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ViewPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='VIEW')
        super().set_object_identifier(val=object_identifier)

class MaterializedViewPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing MaterializedViewPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='MATERIALIZEDVIEW')
        super().set_object_identifier(val=object_identifier)

class SemanticViewPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing SemanticViewPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SEMANTICVIEW')
        super().set_object_identifier(val=object_identifier)

class NotebookPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing NotebookPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='NOTEBOOK')
        super().set_object_identifier(val=object_identifier)

class SecretPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing SecretPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SECRET')
        super().set_object_identifier(val=object_identifier)

class AggregationPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing AggregationPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='AGGREGATIONPOLICY')
        super().set_object_identifier(val=object_identifier)

class JoinPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing JoinPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='JOINPOLICY')
        super().set_object_identifier(val=object_identifier)

class MaskingPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing MaskingPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='MASKINGPOLICY')
        super().set_object_identifier(val=object_identifier)

class PrivacyPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing PrivacyPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='PRIVACYPOLICY')
        super().set_object_identifier(val=object_identifier)

class ProjectionPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ProjectionPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='PROJECTIONPOLICY')
        super().set_object_identifier(val=object_identifier)

class RowAccessPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing RowAccessPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='ROWACCESSPOLICY')
        super().set_object_identifier(val=object_identifier)

class TagPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing TagPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='TAG')
        super().set_object_identifier(val=object_identifier)

class SequencePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing SequencePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SEQUENCE')
        super().set_object_identifier(val=object_identifier)

class StoredProcedurePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing StoredProcedurePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='STOREDPROCEDURE')
        super().set_object_identifier(val=object_identifier)

class UserDefinedFunctionPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing UserDefinedFunctionPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='USERDEFINEDFUNCTION')
        super().set_object_identifier(val=object_identifier)

class ExternalFunctionPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ExternalFunctionPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='EXTERNALFUNCTION')
        super().set_object_identifier(val=object_identifier)

class DataMetricFunctionPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing DataMetricFunctionPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='DATAMETRICFUNCTION')
        super().set_object_identifier(val=object_identifier)

class AlertPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing AlertPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='ALERT')
        super().set_object_identifier(val=object_identifier)

class ImageRepositoryPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ImageRepositoryPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='IMAGEREPOSITORY')
        super().set_object_identifier(val=object_identifier)

class ServicePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ServicePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SERVICE')
        super().set_object_identifier(val=object_identifier)

class SnapshotPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing SnapshotPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SNAPSHOT')
        super().set_object_identifier(val=object_identifier)

class SnapshotPolicyPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing SnapshotPolicyPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SNAPSHOTPOLICY')
        super().set_object_identifier(val=object_identifier)

class SnapshotSetPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing SnapshotSetPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='SNAPSHOTSET')
        super().set_object_identifier(val=object_identifier)

class StreamlitPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing StreamlitPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='STREAMLIT')
        super().set_object_identifier(val=object_identifier)

class ModelPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ModelPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='MODEL')
        super().set_object_identifier(val=object_identifier)

class CortexSearchServicePrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing CortexSearchServicePrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='CORTEXSEARCHSERVICE')
        super().set_object_identifier(val=object_identifier)

class ContactPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing ContactPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='CONTACT')
        super().set_object_identifier(val=object_identifier)

class DatasetPrivileges(BasePrivilege):
    def __init__(self,session,logger,object_identifier,database,schema):
        logger.info(f"Initializing DatasetPrivileges for {object_identifier} in {database}.{schema}")
        super().__init__(session=session,logger=logger)
        super().set_object_type(val='DATASET')
        super().set_object_identifier(val=object_identifier)
