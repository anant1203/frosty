from .informationschema import InformationSchema

class ValidatePipeLoadColumnList:
    _fn=InformationSchema._validate_pipe_load_fn
    _first_error_message="FIRST_ERROR_MESSAGE"
    _first_error_line_number="FIRST_ERROR_LINE_NUMBER"
    _first_error_character_position="FIRST_ERROR_CHARACTER_POSITION"
    _first_error_column_name="FIRST_ERROR_COLUMN_NAME"
    _error_count="ERROR_COUNT"
    _error_limit="ERROR_LIMIT"
    _row_count="ROW_COUNT"
    _row_parsed="ROW_PARSED"
    _file_name="FILE_NAME"

class InformationSchemaValidatePipeLoad:
    def __init__(self):
        self.columns=ValidatePipeLoadColumnList()
