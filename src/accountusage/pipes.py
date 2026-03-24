import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsagePipes

class Pipes:
    def __init__(self, session):
        self.col = AccountUsagePipes().columns
        self.session = session

    def get_pipes_in_schema(self, catalog_name, schema_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._pipe_catalog) == catalog_name.upper()) &
            (col(self.col._pipe_schema) == schema_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def is_existing_pipe(self, catalog_name, schema_name, pipe_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._pipe_catalog) == catalog_name.upper()) &
            (col(self.col._pipe_schema) == schema_name.upper()) &
            (col(self.col._pipe_name) == pipe_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return len(df) > 0

    def get_pipe(self, catalog_name, schema_name, pipe_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._pipe_catalog) == catalog_name.upper()) &
            (col(self.col._pipe_schema) == schema_name.upper()) &
            (col(self.col._pipe_name) == pipe_name.upper())
        ).collect()
        if df:
            return df[0]
        return None

    def get_autoingest_pipes(self, catalog_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._pipe_catalog) == catalog_name.upper()) &
            (col(self.col._is_autoingest_enabled) == "TRUE") &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_pipes_by_owner(self, catalog_name, owner_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._pipe_catalog) == catalog_name.upper()) &
            (col(self.col._owner) == owner_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_deleted_pipes(self, catalog_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._pipe_catalog) == catalog_name.upper()) &
            col(self.col._deleted).isNotNull()
        ).collect()
        return df
