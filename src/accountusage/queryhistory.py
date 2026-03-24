import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageQueryHistory

class QueryHistory:
    def __init__(self, session):
        self.col = AccountUsageQueryHistory().columns
        self.session = session

    def get_queries_by_user(self, user_name, start_time=None, end_time=None):
        df = self.session.table(self.col._view).filter(col(self.col._user_name) == user_name.upper())
        if start_time:
            df = df.filter(col(self.col._start_time) >= start_time)
        if end_time:
            df = df.filter(col(self.col._start_time) <= end_time)
        return df.collect()

    def get_queries_by_warehouse(self, warehouse_name, start_time=None, end_time=None):
        df = self.session.table(self.col._view).filter(col(self.col._warehouse_name) == warehouse_name.upper())
        if start_time:
            df = df.filter(col(self.col._start_time) >= start_time)
        if end_time:
            df = df.filter(col(self.col._start_time) <= end_time)
        return df.collect()

    def get_failed_queries(self, start_time=None, end_time=None):
        df = self.session.table(self.col._view).filter(col(self.col._execution_status) == "FAIL")
        if start_time:
            df = df.filter(col(self.col._start_time) >= start_time)
        if end_time:
            df = df.filter(col(self.col._start_time) <= end_time)
        return df.collect()

    def get_queries_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._start_time) >= start_time) &
            (col(self.col._start_time) <= end_time)
        ).collect()
        return df

    def get_long_running_queries(self, min_elapsed_ms, start_time=None, end_time=None):
        df = self.session.table(self.col._view).filter(col(self.col._total_elapsed_time) >= min_elapsed_ms)
        if start_time:
            df = df.filter(col(self.col._start_time) >= start_time)
        if end_time:
            df = df.filter(col(self.col._start_time) <= end_time)
        return df.sort(col(self.col._total_elapsed_time).desc()).collect()

    def get_queries_by_type(self, query_type, start_time=None, end_time=None):
        df = self.session.table(self.col._view).filter(col(self.col._query_type) == query_type.upper())
        if start_time:
            df = df.filter(col(self.col._start_time) >= start_time)
        if end_time:
            df = df.filter(col(self.col._start_time) <= end_time)
        return df.collect()

    def get_queries_by_database(self, database_name, start_time=None, end_time=None):
        df = self.session.table(self.col._view).filter(col(self.col._database_name) == database_name.upper())
        if start_time:
            df = df.filter(col(self.col._start_time) >= start_time)
        if end_time:
            df = df.filter(col(self.col._start_time) <= end_time)
        return df.collect()

    def get_credits_by_warehouse(self, warehouse_name, start_time=None, end_time=None):
        df = self.session.table(self.col._view).filter(
            col(self.col._warehouse_name) == warehouse_name.upper()
        ).select(
            col(self.col._query_id),
            col(self.col._start_time),
            col(self.col._credits_used_cloud_services),
            col(self.col._credits_attributed_compute)
        )
        if start_time:
            df = df.filter(col(self.col._start_time) >= start_time)
        if end_time:
            df = df.filter(col(self.col._start_time) <= end_time)
        return df.collect()
