import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaViews

class Views:
    def __init__(self,session):
        self.col=InformationSchemaViews().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_view(self,db_name,schema_name,view_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==view_name.upper())
        ).collect()
        return len(df)>0

    def is_new_view(self,db_name,schema_name,view_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==view_name.upper())
        ).collect()
        return len(df)==0

    def get_all_views_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper())
        ).select(col(self.col._table_name)).collect()
        return df

    def get_view_definition(self,db_name,schema_name,view_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==view_name.upper())
        ).select(col(self.col._view_definition)).collect()
        if len(df)>0:
            return df[0][0]
        return None

    def is_secure_view(self,db_name,schema_name,view_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==view_name.upper())
        ).select(col(self.col._is_secure)).collect()
        if len(df)>0:
            return df[0][0]=="YES"
        return False
