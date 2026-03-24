import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaClassInstanceFunctions

class ClassInstanceFunctions:
    def __init__(self,session):
        self.col=InformationSchemaClassInstanceFunctions().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_functions_for_instance(self,db_name,schema_name,instance_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._instance_catalog)==db_name.upper()) &
            (col(self.col._instance_schema)==schema_name.upper()) &
            (col(self.col._instance_name)==instance_name.upper())
        ).collect()
        return df

    def get_all_class_instance_functions_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._instance_catalog)==db_name.upper()) &
            (col(self.col._instance_schema)==schema_name.upper())
        ).collect()
        return df
