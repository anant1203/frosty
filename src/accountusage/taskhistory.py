import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageTaskHistory

class TaskHistory:
    def __init__(self, session):
        self.col = AccountUsageTaskHistory().columns
        self.session = session

    def get_task_history_by_name(self, database_name, schema_name, task_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._name) == task_name.upper())
        ).collect()
        return df

    def get_failed_tasks(self):
        df = self.session.table(self.col._view).filter(
            col(self.col._state) == "FAILED"
        ).collect()
        return df

    def get_task_history_in_time_range(self, start_time, end_time):
        df = self.session.table(self.col._view).filter(
            (col(self.col._scheduled_time) >= start_time) &
            (col(self.col._scheduled_time) <= end_time)
        ).collect()
        return df

    def get_task_history_by_state(self, state):
        df = self.session.table(self.col._view).filter(
            col(self.col._state) == state.upper()
        ).collect()
        return df

    def get_task_history_by_schema(self, database_name, schema_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper())
        ).collect()
        return df

    def get_most_recent_run(self, database_name, schema_name, task_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._database_name) == database_name.upper()) &
            (col(self.col._schema_name) == schema_name.upper()) &
            (col(self.col._name) == task_name.upper())
        ).sort(col(self.col._scheduled_time).desc()).limit(1).collect()
        if df:
            return df[0]
        return None
