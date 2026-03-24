import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaExternalTableFileRegistrationHistory

class ExternalTableFileRegistrationHistory:
    def __init__(self,session):
        self.col=InformationSchemaExternalTableFileRegistrationHistory().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_external_table_file_registration_history(self,db_name,result_limit=100):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(RESULT_LIMIT => {result_limit}))").collect()
        return df
