import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageDatabases

class Databases:
    def __init__(self, session):
        self.col = AccountUsageDatabases().columns
        self.session = session

    def get_all_active_databases(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def is_existing_database(self, database_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return len(df) > 0

    def get_database(self, database_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._database_name) == database_name.upper()
        ).collect()
        if df:
            return df[0]
        return None

    def get_databases_by_owner(self, owner_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_owner) == owner_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_transient_databases(self):
        df = self.session.table(self.col._view).filter(
            (col(self.col._is_transient) == "YES") &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_deleted_databases(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._deleted).isNotNull()
        ).collect()
        return df
