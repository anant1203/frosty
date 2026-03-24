import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaApplicationSpecifications

class ApplicationSpecifications:
    def __init__(self,session):
        self.col=InformationSchemaApplicationSpecifications().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_specification(self,db_name,application_name,specification_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._application_name)==application_name.upper()) &
            (col(self.col._specification_name)==specification_name.upper())
        ).collect()
        return len(df)>0

    def is_new_specification(self,db_name,application_name,specification_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._application_name)==application_name.upper()) &
            (col(self.col._specification_name)==specification_name.upper())
        ).collect()
        return len(df)==0

    def get_all_specifications_for_application(self,db_name,application_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            col(self.col._application_name)==application_name.upper()
        ).select(col(self.col._specification_name)).collect()
        return df
