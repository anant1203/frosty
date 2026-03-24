from .informationschema import InformationSchema

class SharesColumnList:
    _view=InformationSchema._shares_view
    _share_name="SHARE_NAME"
    _share_owner="SHARE_OWNER"
    _comment="COMMENT"
    _listing_global_name="LISTING_GLOBAL_NAME"
    _created_on="CREATED_ON"
    _kind="KIND"
    _consumer_accounts="CONSUMER_ACCOUNTS"

class InformationSchemaShares:
    def __init__(self):
        self.columns=SharesColumnList()
