import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageGrantsToUsers

class GrantsToUsers:
    def __init__(self, session):
        self.col = AccountUsageGrantsToUsers().columns
        self.session = session

    def get_grants_for_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._grantee_name) == user_name.upper()
        ).collect()
        return df

    def get_active_grants_for_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._grantee_name) == user_name.upper()) &
            col(self.col._deleted_on).isNull()
        ).collect()
        return df

    def get_users_with_role(self, role_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._role) == role_name.upper()) &
            col(self.col._deleted_on).isNull()
        ).collect()
        return df

    def get_grants_by_grantor(self, granted_by):
        df = self.session.table(self.col._view).filter(
            col(self.col._granted_by) == granted_by.upper()
        ).collect()
        return df
