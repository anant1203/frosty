import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaSemanticDimensions

class SemanticDimensions:
    def __init__(self,session):
        self.col=InformationSchemaSemanticDimensions().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_dimensions_for_semantic_view(self,db_name,schema_name,semantic_view_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._semantic_view_catalog)==db_name.upper()) &
            (col(self.col._semantic_view_schema)==schema_name.upper()) &
            (col(self.col._semantic_view_name)==semantic_view_name.upper())
        ).collect()
        return df

    def get_all_semantic_dimensions_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._semantic_view_catalog)==db_name.upper()) &
            (col(self.col._semantic_view_schema)==schema_name.upper())
        ).collect()
        return df
