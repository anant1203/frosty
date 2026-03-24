from src.infschema.tables import Tables
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


def check_table_exists(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a table exists in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_table_exists called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        table_inspector = Tables(session)
        exists = table_inspector.is_existing_table(database_name, schema_name, table_name)
        
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "message": f"Table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking table '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def list_tables_in_schema(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all tables in a schema.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of tables
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_tables_in_schema called for '%s.%s'", database_name, schema_name)
    try:
        session = _get_session(tool_context)
        table_inspector = Tables(session)
        tables = table_inspector.get_all_tables_in_schema(database_name, schema_name)
        
        table_list = [row[0] for row in tables]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "tables": table_list,
            "count": len(table_list),
            "message": f"Found {len(table_list)} table(s) in schema '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing tables in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "tables": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing tables in schema '{database_name.upper()}.{schema_name.upper()}': {str(e)}"
        }


def get_table_properties(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed properties of a table including row count, size, type, and metadata.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with table properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_table_properties called for '%s.%s.%s'", database_name, schema_name, table_name)
    session = _get_session(tool_context)
    table_inspector = Tables(session)

    if not table_inspector.is_existing_table(database_name, schema_name, table_name):
        return {
            "exists": False,
            "message": f"Table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' does not exist"
        }

    try:
        table_inspector.use_database(database_name)
        df = session.table(table_inspector.col._view).filter(
            (col(table_inspector.col._table_catalog) == database_name.upper()) &
            (col(table_inspector.col._table_schema) == schema_name.upper()) &
            (col(table_inspector.col._table_name) == table_name.upper())
        ).select(
            col(table_inspector.col._table_type),
            col(table_inspector.col._is_transient),
            col(table_inspector.col._row_count),
            col(table_inspector.col._bytes),
            col(table_inspector.col._retention_time),
            col(table_inspector.col._table_owner),
            col(table_inspector.col._created),
            col(table_inspector.col._clustering_key),
            col(table_inspector.col._comment)
        ).collect()
        
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "table_name": table_name.upper(),
                "table_type": row[0],
                "is_transient": row[1],
                "row_count": row[2],
                "bytes": row[3],
                "retention_time_days": row[4],
                "owner": row[5],
                "created": str(row[6]),
                "clustering_key": row[7],
                "comment": row[8],
                "message": f"Retrieved properties for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for table '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving table properties: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for table '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving table properties: {str(e)}"
        }


def count_transient_tables(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Count transient tables in a schema.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context
        
    Returns:
        Dictionary with count of transient tables
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("count_transient_tables called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        table_inspector = Tables(session)
        table_inspector.use_database(database_name)

        df = session.table(table_inspector.col._view).filter(
            (col(table_inspector.col._table_catalog) == database_name.upper()) &
            (col(table_inspector.col._table_schema) == schema_name.upper()) &
            (col(table_inspector.col._is_transient) == 'YES')
        ).count()
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "transient_count": df,
            "message": f"Found {df} transient table(s) in schema '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error counting transient tables in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "transient_count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error counting transient tables: {str(e)}"
        }
    except Exception as e:
        logger.error("Error counting transient tables in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "transient_count": 0,
            "error": str(e),
            "message": f"Error counting transient tables: {str(e)}"
        }


def filter_tables_by_size(database_name: str, schema_name: str, min_bytes: int, tool_context: ToolContext) -> dict:
    """
    Filter tables by minimum size in bytes.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        min_bytes: Minimum size in bytes
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered tables
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("filter_tables_by_size called for '%s.%s' with min_bytes=%s", database_name, schema_name, min_bytes)
    session = _get_session(tool_context)
    try:
        table_inspector = Tables(session)
        table_inspector.use_database(database_name)

        df = session.table(table_inspector.col._view).filter(
            (col(table_inspector.col._table_catalog) == database_name.upper()) &
            (col(table_inspector.col._table_schema) == schema_name.upper()) &
            (col(table_inspector.col._bytes) >= min_bytes)
        ).select(
            col(table_inspector.col._table_name),
            col(table_inspector.col._bytes),
            col(table_inspector.col._row_count)
        ).collect()
        
        tables = [{
            "name": row[0],
            "bytes": row[1],
            "row_count": row[2]
        } for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "tables": tables,
            "count": len(tables),
            "min_bytes": min_bytes,
            "message": f"Found {len(tables)} table(s) with size >= {min_bytes} bytes"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering tables by size in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "tables": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering tables: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering tables by size in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "tables": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering tables: {str(e)}"
        }


def get_tables_by_type(database_name: str, schema_name: str, table_type: str, tool_context: ToolContext) -> dict:
    """
    Get tables filtered by type (BASE TABLE, VIEW, etc.).
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_type: Table type to filter by (e.g., 'BASE TABLE', 'VIEW')
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered tables
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_tables_by_type called for '%s.%s' with type '%s'", database_name, schema_name, table_type)
    session = _get_session(tool_context)
    try:
        table_inspector = Tables(session)
        table_inspector.use_database(database_name)

        df = session.table(table_inspector.col._view).filter(
            (col(table_inspector.col._table_catalog) == database_name.upper()) &
            (col(table_inspector.col._table_schema) == schema_name.upper()) &
            (col(table_inspector.col._table_type) == table_type.upper())
        ).select(col(table_inspector.col._table_name)).collect()
        
        table_list = [row[0] for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_type": table_type.upper(),
            "tables": table_list,
            "count": len(table_list),
            "message": f"Found {len(table_list)} table(s) of type '{table_type.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering tables by type in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "tables": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering tables by type: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering tables by type in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "tables": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering tables by type: {str(e)}"
        }
