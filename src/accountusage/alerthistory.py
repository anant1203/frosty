import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageAlertHistory

class AlertHistory:
    def __init__(self, session):
        self.col = AccountUsageAlertHistory().columns
        self.session = session

    def get_alert_history_by_name(self, database_name, schema_name, alert_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._name) == alert_name.upper())
        ).collect()
        return df

    def get_failed_alerts(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._state) == "FAILED"
        ).collect()
        return df

    def get_alert_history_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._scheduled_time) >= start_time) &
            (col(self.col._scheduled_time) <= end_time)
        ).collect()
        return df

    def get_alert_history_by_state(self, state):
        df = self.session.table(self.col._view).filter(
            col(self.col._state) == state.upper()
        ).collect()
        return df

    def get_alert_history_by_schema(self, database_name, schema_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper())
        ).collect()
        return df
