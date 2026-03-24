import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaTypes

class Types:
    def __init__(self,session):
        self.col=InformationSchemaTypes().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_type(self,db_name,schema_name,type_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._type_catalog)==db_name.upper()) &
            (col(self.col._type_schema)==schema_name.upper()) &
            (col(self.col._type_name)==type_name.upper())
        ).collect()
        return len(df)>0

    def is_new_type(self,db_name,schema_name,type_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._type_catalog)==db_name.upper()) &
            (col(self.col._type_schema)==schema_name.upper()) &
            (col(self.col._type_name)==type_name.upper())
        ).collect()
        return len(df)==0

    def get_all_types_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._type_catalog)==db_name.upper()) &
            (col(self.col._type_schema)==schema_name.upper())
        ).select(col(self.col._type_name)).collect()
        return df
