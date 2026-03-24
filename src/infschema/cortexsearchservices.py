import sys 
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaCortexSearch

class CortexSearchServices:
    def __init__(self,session):
        self.col = InformationSchemaCortexSearch().columns
        self.session = session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def is_existing_cortex_search(self,db_name,schema_name,service_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._service_catalog) == db_name.upper()) & (col(self.col._service_schema) == schema_name.upper()) & (col(self.col._service_name) == service_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return False
        elif len(res) > 0:
            return True
        
    def is_new_cortex_search(self,db_name,schema_name,service_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._service_catalog) == db_name.upper()) & (col(self.col._service_schema) == schema_name.upper()) & (col(self.col._service_name) == service_name.upper()))
        res = df.collect()
        if len(res) == 0:
            return True
        elif len(res) > 0:
            return False

    def get_all_cortex_search_in_schema(self,db_name,schema_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter((col(self.col._service_catalog) == db_name.upper()) & (col(self.col._service_schema) == schema_name.upper())).select(col(self.col._service_name)).collect()
        return df

    def get_cortex_search_properties(self,db_name,schema_name,service_name):
        self.use_database(db_name=db_name)
        df = self.session.table(self.col._view).filter(
            (col(self.col._service_catalog) == db_name.upper()) &
            (col(self.col._service_schema) == schema_name.upper()) &
            (col(self.col._service_name) == service_name.upper())
        ).collect()
        if not df:
            return None
        r = df[0]
        c = self.col
        return {
            "service_name": r[c._service_name],
            "created": r[c._created],
            "definition": r[c._definition],
            "search_column": r[c._search_column],
            "attribute_columns": r[c._attribute_columns],
            "columns": r[c._columns],
            "target_lag": r[c._target_lag],
            "warehouse": r[c._warehouse],
            "comment": r[c._comment],
            "service_query_url": r[c._service_query_url],
            "owner": r[c._owner],
            "owner_role_type": r[c._owner_role_type],
            "data_fresh_as_of": r[c._data_fresh_as_of],
            "data_timestamp": r[c._data_timestamp],
            "source_data_bytes": r[c._source_data_bytes],
            "source_data_num_rows": r[c._source_data_num_rows],
            "indexing_state": r[c._indexing_state],
            "indexing_error": r[c._indexing_error],
            "serving_state": r[c._serving_state],
            "serving_data_bytes": r[c._serving_data_bytes],
            "embedding_model": r[c._embedding_model],
        }
