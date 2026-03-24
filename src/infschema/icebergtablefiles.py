import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaIcebergTableFiles

class IcebergTableFiles:
    def __init__(self,session):
        self.col=InformationSchemaIcebergTableFiles().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_iceberg_table_files(self,db_name,table_name):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(TABLE_NAME => '{table_name}'))").collect()
        return df
