import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaElementTypes

class ElementTypes:
    def __init__(self,session):
        self.col=InformationSchemaElementTypes().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_element_types_for_object(self,db_name,schema_name,object_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._object_catalog)==db_name.upper()) &
            (col(self.col._object_schema)==schema_name.upper()) &
            (col(self.col._object_name)==object_name.upper())
        ).collect()
        return df

    def get_all_element_types_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._object_catalog)==db_name.upper()) &
            (col(self.col._object_schema)==schema_name.upper())
        ).collect()
        return df
