from src.infschema.objectprivileges import ObjectPrivileges
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


def list_object_privileges(object_name: str, object_type: str, tool_context: ToolContext) -> dict:
    """
    List privileges for a specific object.

    Args:
        object_name: Name of the object
        object_type: Type of the object
        tool_context: ADK tool context

    Returns:
        Dictionary with object privileges
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_object_privileges called for '%s' of type '%s'", object_name, object_type)
    session = _get_session(tool_context)
    try:
        inspector = ObjectPrivileges(session)
        df = inspector.get_privileges_for_object(object_name, object_type)
        records = [row.as_dict() for row in df]
        return {"object_name": object_name.upper(), "object_type": object_type.upper(), "records": records, "count": len(records), "message": f"Found {len(records)} privilege(s) for {object_type.upper()} '{object_name.upper()}'"}
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_object_privileges: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_object_privileges: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def list_privileges_for_grantee(grantee: str, tool_context: ToolContext) -> dict:
    """
    List all privileges granted to a specific grantee.

    Args:
        grantee: Name of the grantee
        tool_context: ADK tool context

    Returns:
        Dictionary with privileges for the grantee
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_privileges_for_grantee called for '%s'", grantee)
    session = _get_session(tool_context)
    try:
        inspector = ObjectPrivileges(session)
        df = inspector.get_privileges_for_grantee(grantee)
        records = [row.as_dict() for row in df]
        return {"grantee": grantee.upper(), "records": records, "count": len(records), "message": f"Found {len(records)} privilege(s) for grantee '{grantee.upper()}'"}
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_privileges_for_grantee: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_privileges_for_grantee: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}
