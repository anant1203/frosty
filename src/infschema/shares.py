import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaShares

class Shares:
    def __init__(self,session):
        self.col=InformationSchemaShares().columns
        self.session=session

    def get_all_shares(self):
        df=self.session.table(self.col._view).collect()
        return df

    def is_existing_share(self,share_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._share_name)==share_name.upper()
        ).collect()
        return len(df)>0

    def is_new_share(self,share_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._share_name)==share_name.upper()
        ).collect()
        return len(df)==0

    def get_share_owner(self,share_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._share_name)==share_name.upper()
        ).select(col(self.col._share_owner)).collect()
        if len(df)>0:
            return df[0][0]
        return None
