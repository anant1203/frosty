from .informationschema import InformationSchema

class ListingRefreshHistoryColumnList:
    _fn=InformationSchema._listing_refresh_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _listing_name="LISTING_NAME"
    _status="STATUS"
    _refresh_type="REFRESH_TYPE"

class InformationSchemaListingRefreshHistory:
    def __init__(self):
        self.columns=ListingRefreshHistoryColumnList()
