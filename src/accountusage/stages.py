import sys
import os

from snowflake.snowpark.functions import col

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from src.vars.gvaccountusage import AccountUsageStages

class Stages:
    def __init__(self, session):
        self.col = AccountUsageStages().columns
        self.session = session

    def get_stages_in_schema(self, catalog_name, schema_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._stage_catalog) == catalog_name.upper()) &
            (col(self.col._stage_schema) == schema_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_stages_in_database(self, catalog_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._stage_catalog) == catalog_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def is_existing_stage(self, catalog_name, schema_name, stage_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._stage_catalog) == catalog_name.upper()) &
            (col(self.col._stage_schema) == schema_name.upper()) &
            (col(self.col._stage_name) == stage_name.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return len(df) > 0

    def get_stages_by_type(self, stage_type):
        df = self.session.table(self.col._view).filter(
            (col(self.col._stage_type) == stage_type.upper()) &
            col(self.col._deleted).isNull()
        ).collect()
        return df

    def get_stage(self, catalog_name, schema_name, stage_name):
        df = self.session.table(self.col._view).filter(
            (col(self.col._stage_catalog) == catalog_name.upper()) &
            (col(self.col._stage_schema) == schema_name.upper()) &
            (col(self.col._stage_name) == stage_name.upper())
        ).collect()
        if df:
            return df[0]
        return None
