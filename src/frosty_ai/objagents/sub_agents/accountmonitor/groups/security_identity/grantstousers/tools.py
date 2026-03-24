import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.grantstousers import GrantsToUsers


def _get_session(tool_context: ToolContext):
    session_inst = Session()
    session_inst.set_user(tool_context.state.get('user:SNOWFLAKE_USER_NAME'))
    session_inst.set_account(tool_context.state.get('app:ACCOUNT_IDENTIFIER'))
    session_inst.set_password(tool_context.state.get('user:USER_PASSWORD'))
    if tool_context.state.get('user:AUTHENTICATOR'):
        session_inst.set_authenticator(tool_context.state.get('user:AUTHENTICATOR'))
    if tool_context.state.get('user:ROLE'):
        session_inst.set_role(tool_context.state.get('user:ROLE'))
    if tool_context.state.get('app:WAREHOUSE'):
        session_inst.set_warehouse(tool_context.state.get('app:WAREHOUSE'))
    if tool_context.state.get('app:DATABASE'):
        session_inst.set_database(tool_context.state.get('app:DATABASE'))
    return session_inst.get_session()


def get_grants_for_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get all grants (including deleted) for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with grant records for the user
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_grants_for_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToUsers(session)
        records = inspector.get_grants_for_user(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} grant(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_grants_for_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_grants_for_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_active_grants_for_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get all active (non-deleted) grants for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with active grant records for the user
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_active_grants_for_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToUsers(session)
        records = inspector.get_active_grants_for_user(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} active grant(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_active_grants_for_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_active_grants_for_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_users_with_role(role_name: str, tool_context: ToolContext) -> dict:
    """
    Get all users that have been granted a specific role.

    Args:
        role_name: Snowflake role name
        tool_context: ADK tool context

    Returns:
        Dictionary with users holding the specified role
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_users_with_role called for '%s'", role_name)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToUsers(session)
        records = inspector.get_users_with_role(role_name)
        return {
            "role_name": role_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} user(s) with role '{role_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_users_with_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_users_with_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_grants_by_grantor(granted_by: str, tool_context: ToolContext) -> dict:
    """
    Get all user grants issued by a specific grantor.

    Args:
        granted_by: Name of the grantor (user or role that issued the grant)
        tool_context: ADK tool context

    Returns:
        Dictionary with grant records issued by the specified grantor
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_grants_by_grantor called for '%s'", granted_by)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToUsers(session)
        records = inspector.get_grants_by_grantor(granted_by)
        return {
            "granted_by": granted_by.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} grant(s) issued by '{granted_by.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_grants_by_grantor for '%s': %s", granted_by, str(e))
        return {"granted_by": granted_by.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_grants_by_grantor for '%s': %s", granted_by, str(e))
        return {"granted_by": granted_by.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
