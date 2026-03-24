import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageLoadHistory

class LoadHistory:
    def __init__(self, session):
        self.col = AccountUsageLoadHistory().columns
        self.session = session

    def get_load_history_for_table(self, catalog_name, schema_name, table_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._catalog_name) == catalog_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._table_name) == table_name.upper())
        ).collect()
        return df

    def get_failed_loads(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._status) == "LOAD_FAILED"
        ).collect()
        return df

    def get_load_history_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._last_load_time) >= start_time) &
            (col(self.col._last_load_time) <= end_time)
        ).collect()
        return df

    def get_load_history_by_pipe(self, pipe_catalog_name, pipe_schema_name, pipe_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._pipe_catalog_name) == pipe_catalog_name.upper()) &
            (col(self.col._pipe_schema_name) == pipe_schema_name.upper()) &
            (col(self.col._pipe_name) == pipe_name.upper())
        ).collect()
        return df

    def get_load_errors_for_table(self, catalog_name, schema_name, table_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._catalog_name) == catalog_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._table_name) == table_name.upper()) &
            (col(self.col._error_count) > 0)
        ).select(
            col(self.col._file_name),
            col(self.col._last_load_time),
            col(self.col._status),
            col(self.col._first_error_message),
            col(self.col._first_error_line_number),
            col(self.col._first_error_character_position),
            col(self.col._first_error_col_name),
            col(self.col._error_count),
            col(self.col._error_limit)
        ).collect()
        return df
