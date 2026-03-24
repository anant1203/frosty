import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaEnabledRoles

class EnabledRoles:
    def __init__(self,session):
        self.col=InformationSchemaEnabledRoles().columns
        self.session=session

    def get_all_enabled_roles(self):
        df=self.session.table(self.col._view).collect()
        return df

    def is_role_enabled(self,role_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._role_name)==role_name.upper()
        ).collect()
        return len(df)>0
