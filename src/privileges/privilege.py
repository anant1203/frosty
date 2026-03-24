



from .objectprivilege import (
    DatabasePrivileges,
    UserPrivileges,
    StagePrivileges,
    WarehousePrivileges,
    SchemaPrivileges,
    TablePrivileges,
    FileFormatPrivileges,
    SnowpipePrivileges,
    StreamPrivileges,
    TaskPrivileges,
    ResourceMonitorPrivileges,
    RolePrivileges,
    ExternalVolumePrivileges,
    FailoverGroupPrivileges,
    ReplicationGroupPrivileges,
    IntegrationPrivileges,
    NetworkPolicyPrivileges,
    DataExchangePrivileges,
    ListingPrivileges,
    OrganizationProfilePrivileges,
    ConnectionPrivileges,
    ComputePoolPrivileges,
    ProvisionedThroughputPrivileges,
    ApplicationPackagePrivileges,
    DatabaseRolePrivileges,
    AuthenticationPolicyPrivileges,
    NetworkRulePrivileges,
    PackagesPolicyPrivileges,
    PasswordPolicyPrivileges,
    SessionPolicyPrivileges,
    DynamicTablePrivileges,
    EventTablePrivileges,
    ExternalTablePrivileges,
    HybridTablePrivileges,
    IcebergTablePrivileges,
    ViewPrivileges,
    MaterializedViewPrivileges,
    SemanticViewPrivileges,
    NotebookPrivileges,
    SecretPrivileges,
    AggregationPolicyPrivileges,
    JoinPolicyPrivileges,
    MaskingPolicyPrivileges,
    PrivacyPolicyPrivileges,
    ProjectionPolicyPrivileges,
    RowAccessPolicyPrivileges,
    TagPrivileges,
    SequencePrivileges,
    StoredProcedurePrivileges,
    UserDefinedFunctionPrivileges,
    ExternalFunctionPrivileges,
    DataMetricFunctionPrivileges,
    AlertPrivileges,
    ImageRepositoryPrivileges,
    ServicePrivileges,
    SnapshotPrivileges,
    SnapshotPolicyPrivileges,
    SnapshotSetPrivileges,
    StreamlitPrivileges,
    ModelPrivileges,
    CortexSearchServicePrivileges,
    ContactPrivileges,
    DatasetPrivileges,
)

from src.exception.privilegeexception import ObjectNotSupported
class Privilege:
    def __init__(self,session,logger,object_type,object_identifier,database,schema):
        object_type = object_type.replace(' ','')

        logger.info(f"inside privilege for {object_type} : {object_identifier}")
        logger.info(f" database {database}: , schema: {schema}")
        if object_type.upper()=='DATABASE':
            self.obj=DatabasePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper()=='SCHEMA':
            self.obj=SchemaPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database)
        elif object_type.upper()=='WAREHOUSE':
            self.obj=WarehousePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper()=='STAGE':
            self.obj=StagePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper()=='TABLE':
            self.obj=TablePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper()=='FILEFORMAT' or object_type.upper()=='FILE_FORMAT':
            self.obj=FileFormatPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper()=='SNOWPIPE':
            self.obj=SnowpipePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper()=='STREAM':
            self.obj=StreamPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper()=='TASK':
            self.obj=TaskPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper()=='USER':
            self.obj=UserPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'RESOURCEMONITOR' or object_type.upper() == 'RESOURCE_MONITOR' or object_type.upper() == 'RESOURCE MONITOR':
            logger.info("Object type is Resource Monitor, initializing ResourceMonitorPrivileges")
            self.obj=ResourceMonitorPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'ROLE':
            self.obj=RolePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'EXTERNALVOLUME':
            self.obj=ExternalVolumePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'FAILOVERGROUP':
            self.obj=FailoverGroupPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'REPLICATIONGROUP':
            self.obj=ReplicationGroupPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'INTEGRATION':
            self.obj=IntegrationPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'NETWORKPOLICY':
            self.obj=NetworkPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'DATAEXCHANGE':
            self.obj=DataExchangePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'LISTING':
            self.obj=ListingPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'ORGANIZATIONPROFILE':
            self.obj=OrganizationProfilePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'CONNECTION':
            self.obj=ConnectionPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'COMPUTEPOOL':
            self.obj=ComputePoolPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'PROVISIONEDTHROUGHPUT':
            self.obj=ProvisionedThroughputPrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'APPLICATIONPACKAGE':
            self.obj=ApplicationPackagePrivileges(session=session,logger=logger,object_identifier=object_identifier)
        elif object_type.upper() == 'DATABASEROLE':
            self.obj=DatabaseRolePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database)
        elif object_type.upper() == 'AUTHENTICATIONPOLICY':
            self.obj=AuthenticationPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'NETWORKRULE':
            self.obj=NetworkRulePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'PACKAGESPOLICY':
            self.obj=PackagesPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'PASSWORDPOLICY':
            self.obj=PasswordPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SESSIONPOLICY':
            self.obj=SessionPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'DYNAMICTABLE':
            self.obj=DynamicTablePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'EVENTTABLE':
            self.obj=EventTablePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'EXTERNALTABLE':
            self.obj=ExternalTablePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'HYBRIDTABLE':
            self.obj=HybridTablePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'ICEBERGTABLE':
            self.obj=IcebergTablePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'VIEW':
            self.obj=ViewPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'MATERIALIZEDVIEW':
            self.obj=MaterializedViewPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SEMANTICVIEW':
            self.obj=SemanticViewPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'NOTEBOOK':
            self.obj=NotebookPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SECRET':
            self.obj=SecretPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'AGGREGATIONPOLICY':
            self.obj=AggregationPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'JOINPOLICY':
            self.obj=JoinPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'MASKINGPOLICY':
            self.obj=MaskingPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'PRIVACYPOLICY':
            self.obj=PrivacyPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'PROJECTIONPOLICY':
            self.obj=ProjectionPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'ROWACCESSPOLICY':
            self.obj=RowAccessPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'TAG':
            self.obj=TagPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SEQUENCE':
            self.obj=SequencePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'STOREDPROCEDURE':
            self.obj=StoredProcedurePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'USERDEFINEDFUNCTION':
            self.obj=UserDefinedFunctionPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'EXTERNALFUNCTION':
            self.obj=ExternalFunctionPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'DATAMETRICFUNCTION':
            self.obj=DataMetricFunctionPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'ALERT':
            self.obj=AlertPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'IMAGEREPOSITORY':
            self.obj=ImageRepositoryPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SERVICE':
            self.obj=ServicePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SNAPSHOT':
            self.obj=SnapshotPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SNAPSHOTPOLICY':
            self.obj=SnapshotPolicyPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'SNAPSHOTSET':
            self.obj=SnapshotSetPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'STREAMLIT':
            self.obj=StreamlitPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'MODEL':
            self.obj=ModelPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'CORTEXSEARCHSERVICE':
            self.obj=CortexSearchServicePrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'CONTACT':
            self.obj=ContactPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        elif object_type.upper() == 'DATASET':
            self.obj=DatasetPrivileges(session=session,logger=logger,object_identifier=object_identifier,database=database,schema=schema)
        else:
            raise ObjectNotSupported(object_type=object_type.upper())

    def find_privileges(self):
        self.obj.logger.info(f"finding possible privileges for {self.obj.attr.object_type} : {self.obj.attr.object_identifier}")
        return self.obj.get_allowed_privileges()
    
    def grant_privilege(self,privilege_type,role):
        self.obj.grant_privilege_on_object_to_role(privlege_type=privilege_type,role=role)
        
        