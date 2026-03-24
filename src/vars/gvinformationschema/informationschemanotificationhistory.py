from .informationschema import InformationSchema

class NotificationHistoryColumnList:
    _fn=InformationSchema._notification_history_fn
    _created="CREATED"
    _processed="PROCESSED"
    _message_source="MESSAGE_SOURCE"
    _integration_name="INTEGRATION_NAME"
    _message="MESSAGE"
    _status="STATUS"
    _error_message="ERROR_MESSAGE"

class InformationSchemaNotificationHistory:
    def __init__(self):
        self.columns=NotificationHistoryColumnList()
