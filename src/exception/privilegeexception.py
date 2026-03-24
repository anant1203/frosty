
from snowchainexception import SnowchainException

class PrivilegeException(SnowchainException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidObject(PrivilegeException):
    def __init__(self, object_type):
        super().__init__(f"Snowflake does not allow granting privilege to {object_type} object type")

class ObjectNotSupported(PrivilegeException):
    def __init__(self, object_type):
        super().__init__(f"Forsty does not support granting privilege to {object_type} object type")
