import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageUsers

class Users:
    def __init__(self, session):
        self.col = AccountUsageUsers().columns
        self.session = session

    def get_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._name) == user_name.upper()
        ).collect()
        if df:
            return df[0]
        return None

    def get_all_active_users(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._deleted_on).isNull()
        ).collect()
        return df

    def get_disabled_users(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._disabled) == True
        ).collect()
        return df

    def is_existing_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._name) == user_name.upper()) &
            col(self.col._deleted_on).isNull()
        ).collect()
        return len(df) > 0

    def get_users_by_default_role(self, role_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._default_role) == role_name.upper()
        ).collect()
        return df

    def get_users_by_default_warehouse(self, warehouse_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._default_warehouse) == warehouse_name.upper()
        ).collect()
        return df

    def get_users_not_logged_in_since(self, since_timestamp):
        df = self.session.table(self.col._view).filter(
            (col(self.col._deleted_on).isNull()) &
            (
                col(self.col._last_success_login).isNull() |
                (col(self.col._last_success_login) < since_timestamp)
            )
        ).collect()
        return df

    def get_user_last_login(self, user_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._name) == user_name.upper()
        ).select(col(self.col._last_success_login)).collect()
        if df:
            return df[0][0]
        return None
