import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaDataMetricFunctionReferences

class DataMetricFunctionReferences:
    def __init__(self,session):
        self.col=InformationSchemaDataMetricFunctionReferences().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_data_metric_function_references(self,db_name,ref_entity_name,ref_entity_domain):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(REF_ENTITY_NAME => '{ref_entity_name}', REF_ENTITY_DOMAIN => '{ref_entity_domain}'))").collect()
        return df
