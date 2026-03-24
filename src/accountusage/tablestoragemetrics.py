import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageTableStorageMetrics

class TableStorageMetrics:
    def __init__(self, session):
        self.col = AccountUsageTableStorageMetrics().columns
        self.session = session

    def get_storage_metrics_for_table(self, table_catalog, table_schema, table_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._table_catalog) == table_catalog.upper()) &
            (col(self.col._table_schema) == table_schema.upper()) &
            (col(self.col._table_name) == table_name.upper())
        ).collect()
        return df

    def get_storage_metrics_for_schema(self, table_catalog, table_schema):
        df = self.session.table(self.col._view).filter(
            (col(self.col._table_catalog) == table_catalog.upper()) &
            (col(self.col._table_schema) == table_schema.upper())
        ).collect()
        return df

    def get_storage_metrics_for_database(self, table_catalog):
        df = self.session.table(self.col._view).filter(
            col(self.col._table_catalog) == table_catalog.upper()
        ).collect()
        return df

    def get_deleted_tables(self, table_catalog):
        df = self.session.table(self.col._view).filter(
            (col(self.col._table_catalog) == table_catalog.upper()) &
            (col(self.col._deleted) == True)
        ).collect()
        return df

    def get_tables_with_failsafe_bytes(self, table_catalog, min_failsafe_bytes):
        df = self.session.table(self.col._view).filter(
            (col(self.col._table_catalog) == table_catalog.upper()) &
            (col(self.col._failsafe_bytes) >= min_failsafe_bytes)
        ).select(
            col(self.col._table_name),
            col(self.col._table_schema),
            col(self.col._failsafe_bytes),
            col(self.col._active_bytes)
        ).sort(col(self.col._failsafe_bytes).desc()).collect()
        return df
