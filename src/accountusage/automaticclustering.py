import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageAutomaticClusteringHistory

class AutomaticClusteringHistory:
    def __init__(self, session):
        self.col = AccountUsageAutomaticClusteringHistory().columns
        self.session = session

    def get_clustering_history_for_table(self, database_name, schema_name, table_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._table_name) == table_name.upper())
        ).collect()
        return df

    def get_clustering_history_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._start_time) >= start_time) &
            (col(self.col._start_time) <= end_time)
        ).collect()
        return df

    def get_total_credits_for_table(self, database_name, schema_name, table_name):
        from snowflake.snowpark.functions import sum as sf_sum
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._table_name) == table_name.upper())
        ).select(sf_sum(col(self.col._credits_used)).alias("TOTAL_CREDITS"))
        res = df.collect()
        if res:
            return res[0][0]
        return None

    def get_clustering_history_by_database(self, database_name):
        df = self.session.table(self.col._view).filter(
            col(self.col._database_name) == database_name.upper()
        ).collect()
        return df
