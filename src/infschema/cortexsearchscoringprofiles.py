import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaCortexSearchServiceScoringProfiles

class CortexSearchScoringProfiles:
    def __init__(self,session):
        self.col=InformationSchemaCortexSearchServiceScoringProfiles().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_scoring_profile(self,db_name,schema_name,service_name,profile_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._service_catalog)==db_name.upper()) &
            (col(self.col._service_schema)==schema_name.upper()) &
            (col(self.col._service_name)==service_name.upper()) &
            (col(self.col._profile_name)==profile_name.upper())
        ).collect()
        return len(df)>0

    def is_new_scoring_profile(self,db_name,schema_name,service_name,profile_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._service_catalog)==db_name.upper()) &
            (col(self.col._service_schema)==schema_name.upper()) &
            (col(self.col._service_name)==service_name.upper()) &
            (col(self.col._profile_name)==profile_name.upper())
        ).collect()
        return len(df)==0

    def get_all_scoring_profiles_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._service_catalog)==db_name.upper()) &
            (col(self.col._service_schema)==schema_name.upper())
        ).select(col(self.col._profile_name)).collect()
        return df
