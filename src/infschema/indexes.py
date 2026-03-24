import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaIndexes

class Indexes:
    def __init__(self,session):
        self.col=InformationSchemaIndexes().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_index(self,db_name,schema_name,table_name,index_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==table_name.upper()) &
            (col(self.col._index_name)==index_name.upper())
        ).collect()
        return len(df)>0

    def is_new_index(self,db_name,schema_name,table_name,index_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==table_name.upper()) &
            (col(self.col._index_name)==index_name.upper())
        ).collect()
        return len(df)==0

    def get_all_indexes_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper())
        ).select(col(self.col._index_name)).collect()
        return df

    def get_indexes_for_table(self,db_name,schema_name,table_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==table_name.upper())
        ).collect()
        return df
