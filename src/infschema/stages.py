import sys 
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaStage
class Stages:
    def __init__(self,session):
        self.col = InformationSchemaStage().columns
        self.session = session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_stage(self,db_name,schema_name,stage_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._stage_catalog) == db_name.upper()) & (col(self.col._stage_schema) == schema_name.upper()) & (col(self.col._stage_name) == stage_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return False
        elif len(res) > 0:
            return True
        
    def is_new_stage(self,db_name,schema_name,stage_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._stage_catalog) == db_name.upper()) & (col(self.col._stage_schema) == schema_name.upper()) & (col(self.col._stage_name) == stage_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return True
        elif len(res) > 0:
            return False