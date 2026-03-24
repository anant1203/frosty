import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageLoginHistory

class LoginHistory:
    def __init__(self, session):
        self.col = AccountUsageLoginHistory().columns
        self.session = session

    def get_logins_by_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._user_name) == user_name.upper()
        ).collect()
        return df

    def get_failed_logins(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._is_success) == "NO"
        ).collect()
        return df

    def get_failed_logins_by_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._user_name) == user_name.upper()) &
            (col(self.col._is_success) == "NO")
        ).collect()
        return df

    def get_logins_by_client_ip(self, client_ip):
        df = self.session.table(self.col._view).filter(
            col(self.col._client_ip) == client_ip
        ).collect()
        return df

    def get_logins_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._event_timestamp) >= start_time) &
            (col(self.col._event_timestamp) <= end_time)
        ).collect()
        return df

    def get_logins_by_client_type(self, client_type):
        df = self.session.table(self.col._view).filter(
            col(self.col._reported_client_type) == client_type.upper()
        ).collect()
        return df
