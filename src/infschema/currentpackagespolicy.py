import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaCurrentPackagesPolicy

class CurrentPackagesPolicy:
    def __init__(self,session):
        self.col=InformationSchemaCurrentPackagesPolicy().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_current_packages_policy(self,db_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).collect()
        return df

    def get_policy_allowlist(self,db_name,policy_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            col(self.col._policy_name)==policy_name.upper()
        ).select(col(self.col._allowlist)).collect()
        if len(df)>0:
            return df[0][0]
        return None
