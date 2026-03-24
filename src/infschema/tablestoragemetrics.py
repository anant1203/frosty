import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaTableStorageMetrics

class TableStorageMetrics:
    def __init__(self,session):
        self.col=InformationSchemaTableStorageMetrics().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_storage_metrics_for_table(self,db_name,schema_name,table_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==table_name.upper())
        ).collect()
        return df

    def get_all_storage_metrics_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper())
        ).collect()
        return df

    def get_active_bytes_for_table(self,db_name,schema_name,table_name):
        self.use_database(db_name=db_name)
        df=self.session.table(self.col._view).filter(
            (col(self.col._table_catalog)==db_name.upper()) &
            (col(self.col._table_schema)==schema_name.upper()) &
            (col(self.col._table_name)==table_name.upper())
        ).select(col(self.col._active_bytes)).collect()
        if len(df)>0:
            return df[0][0]
        return None
