from src.infschema.enabledroles import EnabledRoles
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


def list_enabled_roles(tool_context: ToolContext) -> dict:
    """
    List all enabled role at account level.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with list of enabled role
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_enabled_roles called")
    session = _get_session(tool_context)
    try:
        inspector = EnabledRoles(session)
        df = session.table(inspector.col._view).collect()
        records = [row.as_dict() for row in df]
        return {
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} enabled role record(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_enabled_roles: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_enabled_roles: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}
