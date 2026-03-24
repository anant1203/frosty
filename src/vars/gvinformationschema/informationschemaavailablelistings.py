from .informationschema import InformationSchema

class AvailableListingsColumnList:
    _fn=InformationSchema._available_listings_fn
    _listing_global_name="LISTING_GLOBAL_NAME"
    _title="TITLE"
    _description="DESCRIPTION"
    _provider_account_name="PROVIDER_ACCOUNT_NAME"
    _categories="CATEGORIES"
    _updated_on="UPDATED_ON"

class InformationSchemaAvailableListings:
    def __init__(self):
        self.columns=AvailableListingsColumnList()
