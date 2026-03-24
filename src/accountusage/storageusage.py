import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageStorageUsage

class StorageUsage:
    def __init__(self, session):
        self.col = AccountUsageStorageUsage().columns
        self.session = session

    def get_storage_usage_in_time_range(self, start_date, end_date):
        df = self.session.table(self.col._view).filter(
            (col(self.col._usage_date) >= start_date) &
            (col(self.col._usage_date) <= end_date)
        ).collect()
        return df

    def get_latest_storage_usage(self):
        df = self.session.table(self.col._view).sort(
            col(self.col._usage_date).desc()
        ).limit(1).collect()
        if df:
            return df[0]
        return None

    def get_average_database_bytes_in_range(self, start_date, end_date):
        from snowflake.snowpark.functions import avg
        df = self.session.table(self.col._view).filter(
            (col(self.col._usage_date) >= start_date) &
            (col(self.col._usage_date) <= end_date)
        ).select(avg(col(self.col._average_database_bytes)).alias("AVG_DATABASE_BYTES"))
        res = df.collect()
        if res:
            return res[0][0]
        return None

    def get_all_storage_usage(self):
        df = self.session.table(self.col._view).sort(
            col(self.col._usage_date).desc()
        ).collect()
        return df
