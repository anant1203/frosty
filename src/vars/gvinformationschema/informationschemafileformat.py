from .informationschema import InformationSchema
class FileFormatColumnList:
    _view = InformationSchema._file_format_view
    _file_format_catalog="FILE_FORMAT_CATALOG"
    _file_format_schema="FILE_FORMAT_SCHEMA"
    _file_format_name="FILE_FORMAT_NAME"
    _file_format_owner="FILE_FORMAT_OWNER"
    _file_format_type="FILE_FORMAT_TYPE"
    _record_delimiter="RECORD_DELIMITER"
    _field_delimiter="FIELD_DELIMITER"
    _skip_header="SKIP_HEADER"
    _date_format="DATE_FORMAT"
    _time_format="TIME_FORMAT"
    _timestamp_format="TIMESTAMP_FORMAT"
    _binary_format="BINARY_FORMAT"
    _escape="ESCAPE"
    _escape_unenclosed_field="ESCAPE_UNENCLOSED_FIELD"
    _trim_space="TRIM_SPACE"
    _field_optionally_enclosed_by="FIELD_OPTIONALLY_ENCLOSED_BY"
    _null_if="NULL_IF"
    _compression="COMPRESSION"
    _error_on_column_count_mismatch="ERROR_ON_COLUMN_COUNT_MISMATCH"
    _created="CREATED"
    _last_altered="LAST_ALTERED"
    _comment="COMMENT"

class InformationSchemaFileFormat:
    def __init__(self):
        self.columns=FileFormatColumnList()
