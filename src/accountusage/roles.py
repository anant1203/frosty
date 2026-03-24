import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageRoles

class Roles:
    def __init__(self, session):
        self.col = AccountUsageRoles().columns
        self.session = session

    def get_all_active_roles(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._deleted_on).isNull()
        ).collect()
        return df

    def is_existing_role(self, role_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._name) == role_name.upper()) &
            col(self.col._deleted_on).isNull()
        ).collect()
        return len(df) > 0

    def get_role(self, role_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._name) == role_name.upper()
        ).collect()
        if df:
            return df[0]
        return None

    def get_roles_by_owner(self, owner_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._owner) == owner_name.upper()) &
            col(self.col._deleted_on).isNull()
        ).collect()
        return df

    def get_deleted_roles(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._deleted_on).isNotNull()
        ).collect()
        return df
