from src.infschema.fileformats import FileFormats
from src.session import Session
from google.adk.tools import ToolContext
from snowflake.snowpark.functions import col
from snowflake.snowpark.exceptions import SnowparkSQLException
import logging


def _get_session(tool_context: ToolContext):
    """Helper function to get Snowflake session from tool context."""
    session_inst = Session()
    username = tool_context.state.get('user:SNOWFLAKE_USER_NAME')
    account = tool_context.state.get('app:ACCOUNT_IDENTIFIER')
    session_inst.set_user(username)
    session_inst.set_account(account)
    session_inst.set_password(tool_context.state.get('user:USER_PASSWORD'))
    if tool_context.state.get('user:AUTHENTICATOR'):
        session_inst.set_authenticator(tool_context.state.get('user:AUTHENTICATOR'))
    if tool_context.state.get('user:ROLE'):
        session_inst.set_role(tool_context.state.get('user:ROLE'))
    if tool_context.state.get('app:WAREHOUSE'):
        session_inst.set_warehouse(tool_context.state.get('app:WAREHOUSE'))
    if tool_context.state.get('app:DATABASE'):
        session_inst.set_database(tool_context.state.get('app:DATABASE'))
    session = session_inst.get_session()
    return session


def check_fileformat_exists(database_name: str, schema_name: str, format_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a file format exists in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        format_name: Name of the file format to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_fileformat_exists called for '%s.%s.%s'", database_name, schema_name, format_name)
    try:
        session = _get_session(tool_context)
        fileformat_inspector = FileFormats(session)
        exists = fileformat_inspector.is_existing_file_format(database_name, schema_name, format_name)
        
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "format_name": format_name.upper(),
            "message": f"File format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking file format '%s.%s.%s': %s", database_name, schema_name, format_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "format_name": format_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking file format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}': {str(e)}"
        }


def list_all_fileformats(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all file formats in a schema.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of file formats
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_fileformats called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        fileformat_inspector = FileFormats(session)
        df = fileformat_inspector.get_all_file_formats_in_schema(database_name, schema_name)
        
        formats = [{
            "name": row[0],
            "type": row[1]
        } for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "file_formats": formats,
            "count": len(formats),
            "message": f"Found {len(formats)} file format(s) in schema '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing file formats in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "file_formats": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing file formats: {str(e)}"
        }
    except Exception as e:
        logger.error("Error listing file formats in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "file_formats": [],
            "count": 0,
            "error": str(e),
            "message": f"Error listing file formats: {str(e)}"
        }


def get_fileformat_properties(database_name: str, schema_name: str, format_name: str, tool_context: ToolContext) -> dict:
    """
    Get all properties of a file format including type, delimiters, compression, format options, and timestamps.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        format_name: Name of the file format
        tool_context: ADK tool context
        
    Returns:
        Dictionary with all file format properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_fileformat_properties called for '%s.%s.%s'", database_name, schema_name, format_name)
    session = _get_session(tool_context)
    fileformat_inspector = FileFormats(session)

    if not fileformat_inspector.is_existing_file_format(database_name, schema_name, format_name):
        return {
            "exists": False,
            "message": f"File format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}' does not exist"
        }

    try:
        df = fileformat_inspector.get_file_format_details(database_name, schema_name, format_name)
        
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "format_name": row[0],
                "owner": row[1],
                "format_type": row[2],
                "record_delimiter": row[3],
                "field_delimiter": row[4],
                "skip_header": row[5],
                "date_format": row[6],
                "time_format": row[7],
                "timestamp_format": row[8],
                "binary_format": row[9],
                "escape": row[10],
                "escape_unenclosed_field": row[11],
                "trim_space": row[12],
                "field_optionally_enclosed_by": row[13],
                "null_if": row[14],
                "compression": row[15],
                "error_on_column_count_mismatch": row[16],
                "created": str(row[17]),
                "last_altered": str(row[18]),
                "comment": row[19],
                "message": f"Retrieved properties for file format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for file format '%s.%s.%s': %s", database_name, schema_name, format_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving file format properties: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for file format '%s.%s.%s': %s", database_name, schema_name, format_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving file format properties: {str(e)}"
        }


def filter_fileformats_by_type(database_name: str, schema_name: str, format_type: str, tool_context: ToolContext) -> dict:
    """
    Filter file formats by type (CSV, JSON, PARQUET, etc.).
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        format_type: File format type to filter by (CSV, JSON, PARQUET, AVRO, ORC, XML)
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered file formats
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("filter_fileformats_by_type called for '%s.%s' with type '%s'", database_name, schema_name, format_type)
    session = _get_session(tool_context)
    try:
        fileformat_inspector = FileFormats(session)
        df = fileformat_inspector.get_file_formats_by_type(database_name, schema_name, format_type)
        
        format_list = [row[0] for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "format_type": format_type.upper(),
            "file_formats": format_list,
            "count": len(format_list),
            "message": f"Found {len(format_list)} {format_type.upper()} file format(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering file formats by type in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "file_formats": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering file formats: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering file formats by type in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "file_formats": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering file formats: {str(e)}"
        }


def list_fileformats_by_owner(database_name: str, schema_name: str, owner_role: str, tool_context: ToolContext) -> dict:
    """
    List file formats owned by a specific role.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        owner_role: Name of the role that owns the file formats
        tool_context: ADK tool context
        
    Returns:
        Dictionary with file formats owned by the specified role
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_fileformats_by_owner called for '%s.%s' with owner '%s'", database_name, schema_name, owner_role)
    session = _get_session(tool_context)
    try:
        fileformat_inspector = FileFormats(session)
        df = fileformat_inspector.get_file_formats_by_owner(database_name, schema_name, owner_role)
        
        formats = [{
            "name": row[0],
            "type": row[1]
        } for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "owner_role": owner_role.upper(),
            "file_formats": formats,
            "count": len(formats),
            "message": f"Found {len(formats)} file format(s) owned by role '{owner_role.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing file formats by owner in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "file_formats": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing file formats by owner: {str(e)}"
        }
    except Exception as e:
        logger.error("Error listing file formats by owner in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "file_formats": [],
            "count": 0,
            "error": str(e),
            "message": f"Error listing file formats by owner: {str(e)}"
        }


def get_fileformat_format_options(database_name: str, schema_name: str, format_name: str, tool_context: ToolContext) -> dict:
    """
    Get format-specific parsing options for a file format including date/time formats,
    escape characters, trim settings, null handling, and error handling options.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        format_name: Name of the file format
        tool_context: ADK tool context
        
    Returns:
        Dictionary with format-specific parsing options
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_fileformat_format_options called for '%s.%s.%s'", database_name, schema_name, format_name)
    session = _get_session(tool_context)
    fileformat_inspector = FileFormats(session)

    if not fileformat_inspector.is_existing_file_format(database_name, schema_name, format_name):
        return {
            "exists": False,
            "message": f"File format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}' does not exist"
        }

    try:
        fileformat_inspector.use_database(database_name)
        df = session.table(fileformat_inspector.col._view).filter(
            (col(fileformat_inspector.col._file_format_catalog) == database_name.upper()) &
            (col(fileformat_inspector.col._file_format_schema) == schema_name.upper()) &
            (col(fileformat_inspector.col._file_format_name) == format_name.upper())
        ).select(
            col(fileformat_inspector.col._date_format),
            col(fileformat_inspector.col._time_format),
            col(fileformat_inspector.col._timestamp_format),
            col(fileformat_inspector.col._binary_format),
            col(fileformat_inspector.col._escape),
            col(fileformat_inspector.col._escape_unenclosed_field),
            col(fileformat_inspector.col._trim_space),
            col(fileformat_inspector.col._field_optionally_enclosed_by),
            col(fileformat_inspector.col._null_if),
            col(fileformat_inspector.col._error_on_column_count_mismatch)
        ).collect()
        
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "format_name": format_name.upper(),
                "date_format": row[0],
                "time_format": row[1],
                "timestamp_format": row[2],
                "binary_format": row[3],
                "escape": row[4],
                "escape_unenclosed_field": row[5],
                "trim_space": row[6],
                "field_optionally_enclosed_by": row[7],
                "null_if": row[8],
                "error_on_column_count_mismatch": row[9],
                "message": f"Retrieved format options for file format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving format options for '%s.%s.%s': %s", database_name, schema_name, format_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving format options: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving format options for '%s.%s.%s': %s", database_name, schema_name, format_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving format options: {str(e)}"
        }


def get_fileformat_timestamps(database_name: str, schema_name: str, format_name: str, tool_context: ToolContext) -> dict:
    """
    Get creation and last altered timestamps for a file format.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        format_name: Name of the file format
        tool_context: ADK tool context
        
    Returns:
        Dictionary with created and last_altered timestamps
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_fileformat_timestamps called for '%s.%s.%s'", database_name, schema_name, format_name)
    session = _get_session(tool_context)
    fileformat_inspector = FileFormats(session)

    if not fileformat_inspector.is_existing_file_format(database_name, schema_name, format_name):
        return {
            "exists": False,
            "message": f"File format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}' does not exist"
        }

    try:
        fileformat_inspector.use_database(database_name)
        df = session.table(fileformat_inspector.col._view).filter(
            (col(fileformat_inspector.col._file_format_catalog) == database_name.upper()) &
            (col(fileformat_inspector.col._file_format_schema) == schema_name.upper()) &
            (col(fileformat_inspector.col._file_format_name) == format_name.upper())
        ).select(
            col(fileformat_inspector.col._created),
            col(fileformat_inspector.col._last_altered)
        ).collect()
        
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "format_name": format_name.upper(),
                "created": str(row[0]),
                "last_altered": str(row[1]),
                "message": f"Retrieved timestamps for file format '{database_name.upper()}.{schema_name.upper()}.{format_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving timestamps for '%s.%s.%s': %s", database_name, schema_name, format_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving file format timestamps: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving timestamps for '%s.%s.%s': %s", database_name, schema_name, format_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving file format timestamps: {str(e)}"
        }
