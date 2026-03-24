import sys 
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaTable
class Tables:
    def __init__(self,session):
        self.col = InformationSchemaTable().columns
        self.session = session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_table(self,db_name,schema_name,table_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._table_catalog) == db_name.upper()) & (col(self.col._table_schema) == schema_name.upper()) & (col(self.col._table_name) == table_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return False
        elif len(res) > 0:
            return True
        
    def is_new_table(self,db_name,schema_name,table_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._table_catalog) == db_name.upper()) & (col(self.col._table_schema) == schema_name.upper()) & (col(self.col._table_name) == table_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return True
        elif len(res) > 0:
            return False
        
    def get_all_tables_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._table_catalog)== db_name.upper()) & (col(self.col._table_schema)==schema_name)).select(col(self.col._table_name)).collect()
        return df