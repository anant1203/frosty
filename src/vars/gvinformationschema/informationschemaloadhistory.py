from .informationschema import InformationSchema

class LoadHistoryColumnList:
    _view = f"{InformationSchema._information_schema}.LOAD_HISTORY"
    _schema_name = "SCHEMA_NAME"
    _file_name = "FILE_NAME"
    _table_name = "TABLE_NAME"
    _last_load_time = "LAST_LOAD_TIME"
    _status = "STATUS"
    _row_count = "ROW_COUNT"
    _row_parsed = "ROW_PARSED"
    _first_error_message = "FIRST_ERROR_MESSAGE"
    _first_error_line_number = "FIRST_ERROR_LINE_NUMBER"
    _first_error_character_position = "FIRST_ERROR_CHARACTER_POSITION"
    _first_error_col_name = "FIRST_ERROR_COL_NAME"
    _error_count = "ERROR_COUNT"
    _error_limit = "ERROR_LIMIT"

class InformationSchemaLoadHistory:
    def __init__(self):
        self.columns = LoadHistoryColumnList()
