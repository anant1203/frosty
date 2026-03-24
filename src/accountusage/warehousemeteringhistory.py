import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageWarehouseMeteringHistory

class WarehouseMeteringHistory:
    def __init__(self, session):
        self.col = AccountUsageWarehouseMeteringHistory().columns
        self.session = session

    def get_metering_by_warehouse(self, warehouse_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._warehouse_name) == warehouse_name.upper()
        ).collect()
        return df

    def get_metering_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._start_time) >= start_time) &
            (col(self.col._start_time) <= end_time)
        ).collect()
        return df

    def get_total_credits_by_warehouse(self, warehouse_name):
        from snowflake.snowpark.functions import sum as sf_sum
        df = self.session.table(self.col._view).filter(
            col(self.col._warehouse_name) == warehouse_name.upper()
        ).select(sf_sum(col(self.col._credits_used)).alias("TOTAL_CREDITS_USED"))
        res = df.collect()
        if res:
            return res[0][0]
        return None

    def get_all_warehouse_names(self):
        df = self.session.table(self.col._view).select(
            col(self.col._warehouse_name)
        ).distinct().collect()
        return [r[0] for r in df]

    def get_credits_by_warehouse_in_time_range(self, warehouse_name, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._warehouse_name) == warehouse_name.upper()) &
            (col(self.col._start_time) >= start_time) &
            (col(self.col._start_time) <= end_time)
        ).select(
            col(self.col._start_time),
            col(self.col._end_time),
            col(self.col._credits_used),
            col(self.col._credits_used_compute),
            col(self.col._credits_used_cloud_services)
        ).collect()
        return df
