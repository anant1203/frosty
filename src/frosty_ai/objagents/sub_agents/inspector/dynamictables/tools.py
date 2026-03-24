from src.infschema.dynamictables import DynamicTables
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


def get_dynamic_tables(database_name: str, tool_context: ToolContext) -> dict:
    """
    Get dynamic table for a database.

    Args:
        database_name: Name of the database
        tool_context: ADK tool context

    Returns:
        Dictionary with dynamic table records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_dynamic_tables called for database '%s'", database_name)
    session = _get_session(tool_context)
    try:
        inspector = DynamicTables(session)
        df = inspector.get_dynamic_tables(database_name)
        records = [row.as_dict() for row in df]
        return {
            "database_name": database_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} dynamic table record(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_dynamic_tables: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_dynamic_tables: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}

def check_dynamic_table_exists(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a dynamic table exists.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the dynamic table
        tool_context: ADK tool context

    Returns:
        Dictionary with existence status
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_dynamic_table_exists called for '%s.%s.%s'", database_name, schema_name, table_name)
    session = _get_session(tool_context)
    try:
        inspector = DynamicTables(session)
        df = inspector.get_dynamic_tables(database_name)
        records = [row.as_dict() for row in df]
        exists = any(r.get('TABLE_NAME', r.get('NAME', '')).upper() == table_name.upper() and
                     r.get('TABLE_SCHEMA', r.get('SCHEMA_NAME', '')).upper() == schema_name.upper()
                     for r in records)
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "message": f"Dynamic table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' {'exists' if exists else 'does not exist'}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in check_dynamic_table_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in check_dynamic_table_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}
