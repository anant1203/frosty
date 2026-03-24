import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaTaskDependents

class TaskDependents:
    def __init__(self,session):
        self.col=InformationSchemaTaskDependents().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_task_dependents(self,db_name,task_name):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(TASK_NAME => '{task_name}'))").collect()
        return df
