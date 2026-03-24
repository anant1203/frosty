import sys
import os

from snowflake.snowpark.functions import col
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from src.vars.gvinformationschema import InformationSchemaListings

class Listings:
    def __init__(self,session):
        self.col=InformationSchemaListings().columns
        self.session=session

    def get_all_listings(self):
        df=self.session.table(self.col._view).collect()
        return df

    def is_existing_listing(self,listing_global_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._listing_global_name)==listing_global_name.upper()
        ).collect()
        return len(df)>0

    def is_new_listing(self,listing_global_name):
        df=self.session.table(self.col._view).filter(
            col(self.col._listing_global_name)==listing_global_name.upper()
        ).collect()
        return len(df)==0
