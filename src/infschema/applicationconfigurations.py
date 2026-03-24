import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaApplicationConfigurations

class ApplicationConfigurations:
    def __init__(self,session):
        self.col=InformationSchemaApplicationConfigurations().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_application_configuration(self,db_name,application_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            col(self.col._application_name)==application_name.upper()
        ).collect()
        return len(df)>0

    def is_new_application_configuration(self,db_name,application_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            col(self.col._application_name)==application_name.upper()
        ).collect()
        return len(df)==0

    def get_all_application_configurations(self,db_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).collect()
        return df
