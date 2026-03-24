import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaReplicationGroupRefreshProgress

class ReplicationGroupRefreshProgress:
    def __init__(self,session):
        self.col=InformationSchemaReplicationGroupRefreshProgress().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_replication_group_refresh_progress(self,db_name,replication_group_name):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(REPLICATION_GROUP_NAME => '{replication_group_name}'))").collect()
        return df
