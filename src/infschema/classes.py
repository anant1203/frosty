import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaClasses

class Classes:
    def __init__(self,session):
        self.col=InformationSchemaClasses().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_class(self,db_name,schema_name,class_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._class_catalog)==db_name.upper()) &
            (col(self.col._class_schema)==schema_name.upper()) &
            (col(self.col._class_name)==class_name.upper())
        ).collect()
        return len(df)>0

    def is_new_class(self,db_name,schema_name,class_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._class_catalog)==db_name.upper()) &
            (col(self.col._class_schema)==schema_name.upper()) &
            (col(self.col._class_name)==class_name.upper())
        ).collect()
        return len(df)==0

    def get_all_classes_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._class_catalog)==db_name.upper()) &
            (col(self.col._class_schema)==schema_name.upper())
        ).select(col(self.col._class_name)).collect()
        return df
