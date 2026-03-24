import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaReferentialConstraints

class ReferentialConstraints:
    def __init__(self,session):
        self.col=InformationSchemaReferentialConstraints().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_all_referential_constraints_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._constraint_catalog)==db_name.upper()) &
            (col(self.col._constraint_schema)==schema_name.upper())
        ).collect()
        return df

    def is_existing_referential_constraint(self,db_name,schema_name,constraint_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._constraint_catalog)==db_name.upper()) &
            (col(self.col._constraint_schema)==schema_name.upper()) &
            (col(self.col._constraint_name)==constraint_name.upper())
        ).collect()
        return len(df)>0

    def is_new_referential_constraint(self,db_name,schema_name,constraint_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._constraint_catalog)==db_name.upper()) &
            (col(self.col._constraint_schema)==schema_name.upper()) &
            (col(self.col._constraint_name)==constraint_name.upper())
        ).collect()
        return len(df)==0
