import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageSchemata

class Schemata:
    def __init__(self, session):
        self.col = AccountUsageSchemata().columns
        self.session = session

    def get_schemas_in_database(self, catalog_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._catalog_name) == catalog_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def is_existing_schema(self, catalog_name, schema_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._catalog_name) == catalog_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return len(df) > 0

    def get_schema(self, catalog_name, schema_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._catalog_name) == catalog_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper())
        ).collect()
        if df:
            return df[0]
        return None

    def get_schemas_by_owner(self, owner_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._schema_owner) == owner_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_transient_schemas(self, catalog_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._catalog_name) == catalog_name.upper()) &
            (col(self.col._is_transient) == "YES") &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_deleted_schemas(self, catalog_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._catalog_name) == catalog_name.upper()) &
            col(self.col._deleted).isNotNull()
        ).collect()
        return df
