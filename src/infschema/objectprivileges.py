import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaObjectPrivileges

class ObjectPrivileges:
    def __init__(self,session):
        self.col=InformationSchemaObjectPrivileges().columns
        self.session=session

    def get_all_object_privileges(self):
        df=self.session.table(self.col._view).collect()
        return df

    def get_privileges_for_object(self,object_name,object_type):
        df=self.session.table(self.col._view).filter(
            (col(self.col._object_name)==object_name.upper()) &
            (col(self.col._object_type)==object_type.upper())
        ).collect()
        return df

    def get_privileges_for_grantee(self,grantee):
        df=self.session.table(self.col._view).filter(
            col(self.col._grantee)==grantee.upper()
        ).collect()
        return df
