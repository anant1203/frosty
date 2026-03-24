from src.infschema.columns import Columns
from src.session import Session
from google.adk.tools import ToolContext
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


def check_column_exists(database_name: str, schema_name: str, table_name: str, column_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a column exists in a Snowflake table.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        column_name: Name of the column to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_column_exists called for '%s.%s.%s.%s'", database_name, schema_name, table_name, column_name)
    try:
        session = _get_session(tool_context)
        session.use_database(database_name)
        column_inspector = Columns(session)
        exists = column_inspector.column_exist_in_table(database_name, schema_name, table_name, column_name)

        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "column_name": column_name.upper(),
            "message": f"Column '{column_name.upper()}' {'exists' if exists else 'does not exist'} in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking column '%s' in '%s.%s.%s': %s", column_name, database_name, schema_name, table_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "column_name": column_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking column '{column_name.upper()}' in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def list_columns_in_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    List all columns in a table with their data types.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of columns and their data types
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_columns_in_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        session.use_database(database_name)
        column_inspector = Columns(session)
        columns = column_inspector.get_columns_with_data_types(database_name, schema_name, table_name)

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "columns": columns,
            "count": len(columns),
            "message": f"Found {len(columns)} column(s) in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing columns in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "columns": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing columns in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def get_column_properties(database_name: str, schema_name: str, table_name: str, column_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed properties of a column including data type, nullability, and metadata.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        column_name: Name of the column
        tool_context: ADK tool context
        
    Returns:
        Dictionary with column properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_column_properties called for '%s.%s.%s.%s'", database_name, schema_name, table_name, column_name)
    try:
        session = _get_session(tool_context)
        session.use_database(database_name)
        column_inspector = Columns(session)
        detail = column_inspector.get_column_detail(database_name, schema_name, table_name, column_name)

        if detail is None:
            return {
                "exists": False,
                "message": f"Column '{column_name.upper()}' does not exist in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
            }

        return {
            "exists": True,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "column_name": column_name.upper(),
            "data_type": detail.get("data_type"),
            "is_nullable": detail.get("is_nullable"),
            "ordinal_position": detail.get("ordinal_position"),
            "column_default": detail.get("column_default"),
            "character_maximum_length": detail.get("character_maximum_length"),
            "numeric_precision": detail.get("numeric_precision"),
            "numeric_scale": detail.get("numeric_scale"),
            "is_identity": detail.get("is_identity"),
            "comment": detail.get("comment"),
            "data_type_alias": detail.get("data_type_alias"),
            "schema_evolution_record": detail.get("schema_evolution_record"),
            "message": f"Retrieved properties for column '{column_name.upper()}' in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for column '%s' in '%s.%s.%s': %s", column_name, database_name, schema_name, table_name, str(e))
        return {
            "exists": False,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving column properties: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for column '%s' in '%s.%s.%s': %s", column_name, database_name, schema_name, table_name, str(e))
        return {
            "exists": False,
            "error": str(e),
            "message": f"Error retrieving column properties: {str(e)}"
        }


def get_column_count(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Count the number of columns in a table.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with column count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_column_count called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        session.use_database(database_name)
        column_inspector = Columns(session)
        count = column_inspector.get_column_count(database_name, schema_name, table_name)

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "column_count": count,
            "message": f"Table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' has {count} column(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error counting columns in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "column_count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error counting columns: {str(e)}"
        }
    except Exception as e:
        logger.error("Error counting columns in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "column_count": 0,
            "error": str(e),
            "message": f"Error counting columns: {str(e)}"
        }


def get_nullable_columns(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get all nullable columns in a table.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of nullable columns
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_nullable_columns called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        session.use_database(database_name)
        column_inspector = Columns(session)
        nullable_columns = column_inspector.get_nullable_columns(database_name, schema_name, table_name)

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "nullable_columns": nullable_columns,
            "count": len(nullable_columns),
            "message": f"Found {len(nullable_columns)} nullable column(s) in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error getting nullable columns in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "nullable_columns": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error getting nullable columns: {str(e)}"
        }
    except Exception as e:
        logger.error("Error getting nullable columns in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "nullable_columns": [],
            "count": 0,
            "error": str(e),
            "message": f"Error getting nullable columns: {str(e)}"
        }


def get_all_column_details(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get comprehensive details for all columns in a table including data type, nullability,
    ordinal position, defaults, precision, identity info, comments, and schema evolution records.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with full details for every column in the table
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_all_column_details called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        session.use_database(database_name)
        column_inspector = Columns(session)
        details = column_inspector.get_all_column_details(database_name, schema_name, table_name)

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "columns": details,
            "count": len(details),
            "message": f"Retrieved full details for {len(details)} column(s) in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error getting all column details in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "columns": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error getting all column details: {str(e)}"
        }
    except Exception as e:
        logger.error("Error getting all column details in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "columns": [],
            "count": 0,
            "error": str(e),
            "message": f"Error getting all column details: {str(e)}"
        }


def get_identity_columns(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get all identity columns in a table.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of identity columns
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_identity_columns called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        session.use_database(database_name)
        column_inspector = Columns(session)
        identity_columns = column_inspector.get_identity_columns(database_name, schema_name, table_name)

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "identity_columns": identity_columns,
            "count": len(identity_columns),
            "message": f"Found {len(identity_columns)} identity column(s) in table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error getting identity columns in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "identity_columns": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error getting identity columns: {str(e)}"
        }
    except Exception as e:
        logger.error("Error getting identity columns in '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "identity_columns": [],
            "count": 0,
            "error": str(e),
            "message": f"Error getting identity columns: {str(e)}"
        }
