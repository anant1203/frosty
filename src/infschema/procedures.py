import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaProcedures

class Procedures:
    def __init__(self,session):
        self.col=InformationSchemaProcedures().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_procedure(self,db_name,schema_name,procedure_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._procedure_catalog)==db_name.upper()) &
            (col(self.col._procedure_schema)==schema_name.upper()) &
            (col(self.col._procedure_name)==procedure_name.upper())
        ).collect()
        return len(df)>0

    def is_new_procedure(self,db_name,schema_name,procedure_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._procedure_catalog)==db_name.upper()) &
            (col(self.col._procedure_schema)==schema_name.upper()) &
            (col(self.col._procedure_name)==procedure_name.upper())
        ).collect()
        return len(df)==0

    def get_all_procedures_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._procedure_catalog)==db_name.upper()) &
            (col(self.col._procedure_schema)==schema_name.upper())
        ).select(col(self.col._procedure_name)).collect()
        return df

    def get_procedure_definition(self,db_name,schema_name,procedure_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._procedure_catalog)==db_name.upper()) &
            (col(self.col._procedure_schema)==schema_name.upper()) &
            (col(self.col._procedure_name)==procedure_name.upper())
        ).select(col(self.col._procedure_definition)).collect()
        if len(df)>0:
            return df[0][0]
        return None
