import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaCurrentTaskGraphs

class CurrentTaskGraphs:
    def __init__(self,session):
        self.col=InformationSchemaCurrentTaskGraphs().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_current_task_graphs(self,db_name):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}())").collect()
        return df
