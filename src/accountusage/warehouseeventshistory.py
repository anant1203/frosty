import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageWarehouseEventsHistory

class WarehouseEventsHistory:
    def __init__(self, session):
        self.col = AccountUsageWarehouseEventsHistory().columns
        self.session = session

    def get_events_by_warehouse(self, warehouse_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._warehouse_name) == warehouse_name.upper()
        ).collect()
        return df

    def get_events_by_type(self, event_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._event_name) == event_name.upper()
        ).collect()
        return df

    def get_events_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._timestamp) >= start_time) &
            (col(self.col._timestamp) <= end_time)
        ).collect()
        return df

    def get_events_by_user(self, user_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._user_name) == user_name.upper()
        ).collect()
        return df

    def get_events_by_warehouse_in_time_range(self, warehouse_name, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._warehouse_name) == warehouse_name.upper()) &
            (col(self.col._timestamp) >= start_time) &
            (col(self.col._timestamp) <= end_time)
        ).collect()
        return df
