import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaExternalFunctionsHistory

class ExternalFunctionsHistory:
    def __init__(self,session):
        self.col=InformationSchemaExternalFunctionsHistory().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_external_functions_history(self,db_name,result_limit=100):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(RESULT_LIMIT => {result_limit}))").collect()
        return df
