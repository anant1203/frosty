import sys 
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaSchema

class Schemata:
    def __init__(self,session):
        self.col = InformationSchemaSchema().columns
        self.session = session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col.catalog_name) == db_name.upper()) & (col(self.col.schema_name) == schema_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return False
        elif len(res) > 0:
            return True
        
    def is_new_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col.catalog_name) == db_name.upper()) & (col(self.col.schema_name) == schema_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return True
        elif len(res) > 0:
            return False
