import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageMeteringDailyHistory

class MeteringDailyHistory:
    def __init__(self, session):
        self.col = AccountUsageMeteringDailyHistory().columns
        self.session = session

    def get_metering_in_date_range(self, start_date, end_date):
        df = self.session.table(self.col._view).filter(
            (col(self.col._usage_date) >= start_date) &
            (col(self.col._usage_date) <= end_date)
        ).collect()
        return df

    def get_metering_by_service_type(self, service_type):
        df = self.session.table(self.col._view).filter(
            col(self.col._service_type) == service_type.upper()
        ).collect()
        return df

    def get_metering_by_name(self, name):
        df = self.session.table(self.col._view).filter(
            col(self.col._name) == name.upper()
        ).collect()
        return df

    def get_total_credits_billed_in_date_range(self, start_date, end_date):
        from snowflake.snowpark.functions import sum as sf_sum
        df = self.session.table(self.col._view).filter(
            (col(self.col._usage_date) >= start_date) &
            (col(self.col._usage_date) <= end_date)
        ).select(sf_sum(col(self.col._credits_billed)).alias("TOTAL_CREDITS_BILLED"))
        res = df.collect()
        if res:
            return res[0][0]
        return None

    def get_all_metering_history(self):
        df = self.session.table(self.col._view).sort(
            col(self.col._usage_date).desc()
        ).collect()
        return df
