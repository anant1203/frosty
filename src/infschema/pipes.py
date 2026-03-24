import sys 
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))


from src.vars.gvinformationschema import InformationSchemaPipe
class Pipes:
    def __init__(self,session):
        self.col = InformationSchemaPipe().columns
        self.session = session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_pipe(self,db_name,schema_name,pipe_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._pipe_catalog) == db_name.upper()) & (col(self.col._pipe_schema) == schema_name.upper()) & (col(self.col._pipe_name) == pipe_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return False
        elif len(res) > 0:
            return True
        
    def is_new_pipe(self,db_name,schema_name,pipe_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._pipe_catalog) == db_name.upper()) & (col(self.col._pipe_schema) == schema_name.upper()) & (col(self.col._pipe_name) == pipe_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return True
        elif len(res) > 0:
            return False

    def get_all_pipes_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._pipe_catalog)== db_name.upper()) & (col(self.col._pipe_schema)==schema_name.upper())).select(col(self.col._pipe_name)).collect()
        return df

    def get_pipe_definition(self,db_name,schema_name,pipe_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._pipe_catalog) == db_name.upper()) & (col(self.col._pipe_schema) == schema_name.upper()) & (col(self.col._pipe_name) == pipe_name.upper())).select(col(self.col._definition)).collect()
        if len(df) > 0:
            return df[0][0]
        return None

    def get_pipe_owner(self,db_name,schema_name,pipe_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._pipe_catalog) == db_name.upper()) & (col(self.col._pipe_schema) == schema_name.upper()) & (col(self.col._pipe_name) == pipe_name.upper())).select(col(self.col._pipe_owner)).collect()
        if len(df) > 0:
            return df[0][0]
        return None