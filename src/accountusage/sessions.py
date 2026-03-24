import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageSessions

class Sessions:
    def __init__(self, session):
        self.col = AccountUsageSessions().columns
        self.session = session

    def get_sessions_by_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._user_name) == user_name.upper()
        ).collect()
        return df

    def get_sessions_by_client_application(self, client_application):
        df = self.session.table(self.col._view).filter(
            col(self.col._client_application) == client_application
        ).collect()
        return df

    def get_sessions_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._created_on) >= start_time) &
            (col(self.col._created_on) <= end_time)
        ).collect()
        return df

    def get_sessions_by_authentication_method(self, authentication_method):
        df = self.session.table(self.col._view).filter(
            col(self.col._authentication_method) == authentication_method.upper()
        ).collect()
        return df

    def get_session_by_id(self, session_id):
        df = self.session.table(self.col._view).filter(
            col(self.col._session_id) == session_id
        ).collect()
        if df:
            return df[0]
        return None
