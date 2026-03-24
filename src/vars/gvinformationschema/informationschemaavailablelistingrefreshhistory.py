from .informationschema import InformationSchema

class AvailableListingRefreshHistoryColumnList:
    _fn=InformationSchema._available_listing_refresh_history_fn
    _start_time="START_TIME"
    _end_time="END_TIME"
    _listing_name="LISTING_NAME"
    _status="STATUS"

class InformationSchemaAvailableListingRefreshHistory:
    def __init__(self):
        self.columns=AvailableListingRefreshHistoryColumnList()
