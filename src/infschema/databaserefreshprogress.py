import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaDatabaseRefreshProgress

class DatabaseRefreshProgress:
    def __init__(self,session):
        self.col=InformationSchemaDatabaseRefreshProgress().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_database_refresh_progress(self,db_name,database_name):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(DATABASE_NAME => '{database_name}'))").collect()
        return df
