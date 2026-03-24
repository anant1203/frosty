import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaReplicationGroups

class ReplicationGroups:
    def __init__(self,session):
        self.col=InformationSchemaReplicationGroups().columns
        self.session=session

    def get_all_replication_groups(self):
        df=self.session.table(self.col._view).collect()
        return df

    def is_existing_replication_group(self,replication_group_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._replication_group_name)==replication_group_name.upper()
        ).collect()
        return len(df)>0

    def is_new_replication_group(self,replication_group_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._replication_group_name)==replication_group_name.upper()
        ).collect()
        return len(df)==0
