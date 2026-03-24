import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageGrantsToRoles

class GrantsToRoles:
    def __init__(self, session):
        self.col = AccountUsageGrantsToRoles().columns
        self.session = session

    def get_grants_for_role(self, role_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._grantee_name) == role_name.upper()
        ).collect()
        return df

    def get_grants_by_privilege(self, privilege):
        df = self.session.table(self.col._view).filter(
            col(self.col._privilege) == privilege.upper()
        ).collect()
        return df

    def get_grants_on_object(self, granted_on, object_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._granted_on) == granted_on.upper()) &
            (col(self.col._name) == object_name.upper())
        ).collect()
        return df

    def get_grants_with_grant_option(self, role_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._grantee_name) == role_name.upper()) &
            (col(self.col._grant_option) == "YES")
        ).collect()
        return df

    def get_active_grants_for_role(self, role_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._grantee_name) == role_name.upper()) &
            col(self.col._deleted_on).isNull()
        ).collect()
        return df

    def get_grants_by_grantor(self, granted_by):
        df = self.session.table(self.col._view).filter(
            col(self.col._granted_by) == granted_by.upper()
        ).collect()
        return df
