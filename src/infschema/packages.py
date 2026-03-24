import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaPackages

class Packages:
    def __init__(self,session):
        self.col=InformationSchemaPackages().columns
        self.session=session

    def get_all_packages(self):
        df=self.session.table(self.col._view).collect()
        return df

    def is_existing_package(self,package_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._package_name)==package_name
        ).collect()
        return len(df)>0

    def get_package_versions(self,package_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._package_name)==package_name
        ).select(col(self.col._version)).collect()
        return df
