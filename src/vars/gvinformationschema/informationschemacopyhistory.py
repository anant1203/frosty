from .informationschema import InformationSchema

class CopyHistoryColumnList:
    _fn=InformationSchema._copy_history_fn
    _file_name="FILE_NAME"
    _stage_location="STAGE_LOCATION"
    _last_load_time="LAST_LOAD_TIME"
    _row_count="ROW_COUNT"
    _row_parsed="ROW_PARSED"
    _file_size="FILE_SIZE"
    _first_error_message="FIRST_ERROR_MESSAGE"
    _first_error_line_number="FIRST_ERROR_LINE_NUMBER"
    _first_error_character_position="FIRST_ERROR_CHARACTER_POSITION"
    _first_error_column_name="FIRST_ERROR_COLUMN_NAME"
    _error_count="ERROR_COUNT"
    _error_limit="ERROR_LIMIT"
    _status="STATUS"
    _table_catalog_name="TABLE_CATALOG_NAME"
    _table_schema_name="TABLE_SCHEMA_NAME"
    _table_name="TABLE_NAME"
    _pipe_catalog_name="PIPE_CATALOG_NAME"
    _pipe_schema_name="PIPE_SCHEMA_NAME"
    _pipe_name="PIPE_NAME"
    _pipe_received_time="PIPE_RECEIVED_TIME"

class InformationSchemaCopyHistory:
    def __init__(self):
        self.columns=CopyHistoryColumnList()
