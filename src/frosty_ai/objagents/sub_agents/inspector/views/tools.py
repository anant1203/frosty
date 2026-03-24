from src.infschema.views import Views
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


def check_view_exists(database_name: str, schema_name: str, view_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a view exists.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        view_name: Name of the view
        tool_context: ADK tool context

    Returns:
        Dictionary with existence status
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_view_exists called for '%s.%s.%s'", database_name, schema_name, view_name)
    session = _get_session(tool_context)
    try:
        inspector = Views(session)
        exists = inspector.is_existing_view(database_name, schema_name, view_name)
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "view_name": view_name.upper(),
            "message": f"View '{database_name.upper()}.{schema_name.upper()}.{view_name.upper()}' {'exists' if exists else 'does not exist'}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in check_view_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in check_view_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}

def list_all_views(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all view in a schema.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with list of view
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_views called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        inspector = Views(session)
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._table_catalog) == database_name.upper()) &
            (col(inspector.col._table_schema) == schema_name.upper())
        ).select(col(inspector.col._table_name)).collect()
        view_list = [row[0] for row in df]
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "views": view_list,
            "count": len(view_list),
            "message": f"Found {len(view_list)} view(s) in '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_all_views: %s", str(e))
        return {"views": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_all_views: %s", str(e))
        return {"views": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}

def get_view_properties(database_name: str, schema_name: str, view_name: str, tool_context: ToolContext) -> dict:
    """
    Get properties of a view.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        view_name: Name of the view
        tool_context: ADK tool context

    Returns:
        Dictionary with view properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_view_properties called for '%s.%s.%s'", database_name, schema_name, view_name)
    session = _get_session(tool_context)
    try:
        inspector = Views(session)
        if not inspector.is_existing_view(database_name, schema_name, view_name):
            return {
                "exists": False,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "view_name": view_name.upper(),
                "message": f"View '{database_name.upper()}.{schema_name.upper()}.{view_name.upper()}' not found"
            }
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._table_catalog) == database_name.upper()) &
            (col(inspector.col._table_schema) == schema_name.upper()) &
            (col(inspector.col._table_name) == view_name.upper())
        ).select(
            col(inspector.col._view_definition),
            col(inspector.col._check_option),
            col(inspector.col._is_updatable),
            col(inspector.col._insertable_into),
            col(inspector.col._is_secure),
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
                "view_name": view_name.upper(),
                "view_definition": row[0],
                "check_option": row[1],
                "is_updatable": row[2],
                "insertable_into": row[3],
                "is_secure": row[4],
                "created": str(row[5]),
                "last_altered": str(row[6]),
                "comment": row[7],
                "message": f"Retrieved properties for view '{database_name.upper()}.{schema_name.upper()}.{view_name.upper()}'"
            }
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "view_name": view_name.upper(),
            "message": f"View '{database_name.upper()}.{schema_name.upper()}.{view_name.upper()}' not found"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_view_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_view_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}
