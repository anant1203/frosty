import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaReplicationDatabases

class ReplicationDatabases:
    def __init__(self,session):
        self.col=InformationSchemaReplicationDatabases().columns
        self.session=session

    def get_all_replication_databases(self):
        df=self.session.table(self.col._view).collect()
        return df

    def is_existing_replication_database(self,database_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._database_name)==database_name.upper()
        ).collect()
        return len(df)>0

    def is_new_replication_database(self,database_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._database_name)==database_name.upper()
        ).collect()
        return len(df)==0

    def get_primary_replication_databases(self):
        df=self.session.table(self.col._view).filter(
            col(self.col._is_primary)=="YES"
        ).collect()
        return df
