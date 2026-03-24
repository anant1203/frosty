import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageDataTransferHistory

class DataTransferHistory:
    def __init__(self, session):
        self.col = AccountUsageDataTransferHistory().columns
        self.session = session

    def get_transfers_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._start_time) >= start_time) &
            (col(self.col._start_time) <= end_time)
        ).collect()
        return df

    def get_transfers_by_source_cloud(self, source_cloud):
        df = self.session.table(self.col._view).filter(
            col(self.col._source_cloud) == source_cloud.upper()
        ).collect()
        return df

    def get_transfers_by_target_cloud(self, target_cloud):
        df = self.session.table(self.col._view).filter(
            col(self.col._target_cloud) == target_cloud.upper()
        ).collect()
        return df

    def get_transfers_by_type(self, transfer_type):
        df = self.session.table(self.col._view).filter(
            col(self.col._transfer_type) == transfer_type.upper()
        ).collect()
        return df

    def get_total_bytes_transferred_in_range(self, start_time, end_time):
        from snowflake.snowpark.functions import sum as sf_sum
        df = self.session.table(self.col._view).filter(
            (col(self.col._start_time) >= start_time) &
            (col(self.col._start_time) <= end_time)
        ).select(sf_sum(col(self.col._bytes_transferred)).alias("TOTAL_BYTES"))
        res = df.collect()
        if res:
            return res[0][0]
        return None
