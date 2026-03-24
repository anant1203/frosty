import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageAccessHistory

class AccessHistory:
    def __init__(self, session):
        self.col = AccountUsageAccessHistory().columns
        self.session = session

    def get_access_history_by_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._user_name) == user_name.upper()
        ).collect()
        return df

    def get_access_history_by_query(self, query_id):
        df = self.session.table(self.col._view).filter(
            col(self.col._query_id) == query_id
        ).collect()
        return df

    def get_access_history_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._query_start_time) >= start_time) &
            (col(self.col._query_start_time) <= end_time)
        ).collect()
        return df

    def get_access_history_by_query_type(self, query_type):
        df = self.session.table(self.col._view).filter(
            col(self.col._query_type) == query_type.upper()
        ).collect()
        return df

    def get_access_history_by_user_in_time_range(self, user_name, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._user_name) == user_name.upper()) &
            (col(self.col._query_start_time) >= start_time) &
            (col(self.col._query_start_time) <= end_time)
        ).collect()
        return df
