from .informationschema import InformationSchema

class ListingsColumnList:
    _view=InformationSchema._listings_view
    _listing_id="LISTING_ID"
    _listing_global_name="LISTING_GLOBAL_NAME"
    _title="TITLE"
    _state="STATE"
    _created_on="CREATED_ON"
    _updated_on="UPDATED_ON"
    _published_on="PUBLISHED_ON"
    _provider_account_name="PROVIDER_ACCOUNT_NAME"
    _provider_organization_name="PROVIDER_ORGANIZATION_NAME"

class InformationSchemaListings:
    def __init__(self):
        self.columns=ListingsColumnList()
