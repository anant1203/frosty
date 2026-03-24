import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageServerlessTaskHistory

class ServerlessTaskHistory:
    def __init__(self, session):
        self.col = AccountUsageServerlessTaskHistory().columns
        self.session = session

    def get_history_for_task(self, database_name, schema_name, task_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._task_name) == task_name.upper())
        ).collect()
        return df

    def get_history_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._start_time) >= start_time) &
            (col(self.col._start_time) <= end_time)
        ).collect()
        return df

    def get_total_credits_for_task(self, database_name, schema_name, task_name):
        from snowflake.snowpark.functions import sum as sf_sum
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._task_name) == task_name.upper())
        ).select(sf_sum(col(self.col._credits_used)).alias("TOTAL_CREDITS"))
        res = df.collect()
        if res:
            return res[0][0]
        return None

    def get_history_by_database(self, database_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._database_name) == database_name.upper()
        ).collect()
        return df
