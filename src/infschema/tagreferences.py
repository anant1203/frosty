import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaTagReferences

class TagReferences:
    def __init__(self,session):
        self.col=InformationSchemaTagReferences().columns
        self.session=session

    def use_database(self,db_name):
        self.session.sql(f'USE DATABASE {db_name}').collect()

    def get_tag_references(self,db_name,tag_name):
        self.use_database(db_name=db_name)
        df=self.session.sql(f"SELECT * FROM TABLE({self.col._fn}(TAG_NAME => '{tag_name}'))").collect()
        return df
