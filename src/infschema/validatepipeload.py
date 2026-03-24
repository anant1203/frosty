import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaValidatePipeLoad

class ValidatePipeLoad:
    def __init__(self,session):
        self.col=InformationSchemaValidatePipeLoad().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_validate_pipe_load(self,db_name,pipe_name,start_time):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(PIPE_NAME => '{pipe_name}', START_TIME => '{start_time}'::TIMESTAMP_LTZ))").collect()
        return df
