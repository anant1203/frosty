import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaStageDirectoryFileRegistrationHistory

class StageDirectoryFileRegistrationHistory:
    def __init__(self,session):
        self.col=InformationSchemaStageDirectoryFileRegistrationHistory().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_stage_directory_file_registration_history(self,db_name,stage_name,result_limit=100):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(STAGE_NAME => '{stage_name}', RESULT_LIMIT => {result_limit}))").collect()
        return df
