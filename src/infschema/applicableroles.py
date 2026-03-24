import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaApplicableRoles

class ApplicableRoles:
    def __init__(self,session):
        self.col=InformationSchemaApplicableRoles().columns
        self.session=session

    def get_all_applicable_roles(self):
        df=self.session.table(self.col._view).collect()
        return df

    def is_role_applicable(self,role_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._role_name)==role_name.upper()
        ).collect()
        return len(df)>0
