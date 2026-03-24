from src.infschema.hybridtables import HybridTables
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


def check_hybrid_table_exists(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a hybrid table exists.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the hybrid table
        tool_context: ADK tool context

    Returns:
        Dictionary with existence status
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_hybrid_table_exists called for '%s.%s.%s'", database_name, schema_name, table_name)
    session = _get_session(tool_context)
    try:
        inspector = HybridTables(session)
        exists = inspector.is_existing_hybrid_table(database_name, schema_name, table_name)
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "message": f"Hybrid table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' {'exists' if exists else 'does not exist'}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in check_hybrid_table_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in check_hybrid_table_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}

def list_all_hybrid_tables(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all hybrid table in a schema.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with list of hybrid table
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_hybrid_tables called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        inspector = HybridTables(session)
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._table_catalog) == database_name.upper()) &
            (col(inspector.col._table_schema) == schema_name.upper())
        ).select(col(inspector.col._table_name)).collect()
        table_list = [row[0] for row in df]
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "hybrid_tables": table_list,
            "count": len(table_list),
            "message": f"Found {len(table_list)} hybrid table(s) in '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_all_hybrid_tables: %s", str(e))
        return {"hybrid_tables": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_all_hybrid_tables: %s", str(e))
        return {"hybrid_tables": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}

def get_hybrid_table_properties(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get properties of a hybrid table.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the hybrid table
        tool_context: ADK tool context

    Returns:
        Dictionary with hybrid table properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_hybrid_table_properties called for '%s.%s.%s'", database_name, schema_name, table_name)
    session = _get_session(tool_context)
    try:
        inspector = HybridTables(session)
        if not inspector.is_existing_hybrid_table(database_name, schema_name, table_name):
            return {
                "exists": False,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "table_name": table_name.upper(),
                "message": f"Hybrid table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' not found"
            }
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._table_catalog) == database_name.upper()) &
            (col(inspector.col._table_schema) == schema_name.upper()) &
            (col(inspector.col._table_name) == table_name.upper())
        ).select(
            col(inspector.col._table_owner),
            col(inspector.col._created),
            col(inspector.col._last_altered),
            col(inspector.col._comment)
        ).collect()
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "table_name": table_name.upper(),
                "owner": row[0],
                "created": str(row[1]),
                "last_altered": str(row[2]),
                "comment": row[3],
                "message": f"Retrieved properties for hybrid table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
            }
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "message": f"Hybrid table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' not found"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_hybrid_table_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_hybrid_table_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}
