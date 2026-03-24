import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaQueryHistory

class QueryHistory:
    def __init__(self,session):
        self.col=InformationSchemaQueryHistory().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_query_history(self,db_name,result_limit=100,start_time=None,end_time=None):
        self.use_database(db_name=db_name)
        base = f"SELECT * FROM TABLE({self.col._fn}(RESULT_LIMIT => {result_limit}))"
        if start_time and end_time:
            df=self.session.sql(f"{base} WHERE {self.col._start_time} >= '{start_time}'::TIMESTAMP_LTZ AND {self.col._end_time} <= '{end_time}'::TIMESTAMP_LTZ").collect()
        elif start_time:
            df=self.session.sql(f"{base} WHERE {self.col._start_time} >= '{start_time}'::TIMESTAMP_LTZ").collect()
        elif end_time:
            df=self.session.sql(f"{base} WHERE {self.col._end_time} <= '{end_time}'::TIMESTAMP_LTZ").collect()
        else:
            df=self.session.sql(base).collect()
        return df

    def get_query_history_by_status(self,db_name,execution_status,result_limit=100,start_time=None,end_time=None):
        self.use_database(db_name=db_name)
        base = f"SELECT * FROM TABLE({self.col._fn}(RESULT_LIMIT => {result_limit})) WHERE {self.col._execution_status} = '{execution_status.upper()}'"
        if start_time and end_time:
            df=self.session.sql(f"{base} AND {self.col._start_time} >= '{start_time}'::TIMESTAMP_LTZ AND {self.col._end_time} <= '{end_time}'::TIMESTAMP_LTZ").collect()
        elif start_time:
            df=self.session.sql(f"{base} AND {self.col._start_time} >= '{start_time}'::TIMESTAMP_LTZ").collect()
        elif end_time:
            df=self.session.sql(f"{base} AND {self.col._end_time} <= '{end_time}'::TIMESTAMP_LTZ").collect()
        else:
            df=self.session.sql(base).collect()
        return df
