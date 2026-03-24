from .accountusage import AccountUsage

class AccessHistoryColumnList:
    _view = AccountUsage._access_history_view
    _query_id = "QUERY_ID"
    _query_start_time = "QUERY_START_TIME"
    _user_name = "USER_NAME"
    _direct_objects_accessed = "DIRECT_OBJECTS_ACCESSED"
    _base_objects_accessed = "BASE_OBJECTS_ACCESSED"
    _objects_modified = "OBJECTS_MODIFIED"
    _object_modified_by_ddl = "OBJECT_MODIFIED_BY_DDL"
    _policies_referenced = "POLICIES_REFERENCED"
    _query_type = "QUERY_TYPE"

class AccountUsageAccessHistory:
    def __init__(self):
        self.columns = AccessHistoryColumnList()
