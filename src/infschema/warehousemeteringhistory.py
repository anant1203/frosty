import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaWarehouseMeteringHistory

class WarehouseMeteringHistory:
    def __init__(self,session):
        self.col=InformationSchemaWarehouseMeteringHistory().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_warehouse_metering_history(self,db_name,warehouse_name=None,result_limit=100):
        self.use_database(db_name=db_name)
        if warehouse_name:
            df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(WAREHOUSE_NAME => '{warehouse_name}', RESULT_LIMIT => {result_limit}))").collect()
        else:
            df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(RESULT_LIMIT => {result_limit}))").collect()
        return df
