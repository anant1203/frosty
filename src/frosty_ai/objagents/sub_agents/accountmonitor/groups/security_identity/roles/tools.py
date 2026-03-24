import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.roles import Roles


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


def get_all_active_roles(tool_context: ToolContext) -> dict:
    """
    Get all active (non-deleted) roles in the account.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with all active role records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_all_active_roles called")
    try:
        session = _get_session(tool_context)
        inspector = Roles(session)
        records = inspector.get_all_active_roles()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} active role(s) in the account."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_all_active_roles: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_all_active_roles: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def is_existing_role(role_name: str, tool_context: ToolContext) -> dict:
    """
    Check whether a role exists in the account.

    Args:
        role_name: Snowflake role name
        tool_context: ADK tool context

    Returns:
        Dictionary with an exists boolean and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("is_existing_role called for '%s'", role_name)
    try:
        session = _get_session(tool_context)
        inspector = Roles(session)
        exists = inspector.is_existing_role(role_name)
        return {
            "role_name": role_name.upper(),
            "exists": exists,
            "message": f"Role '{role_name.upper()}' {'exists' if exists else 'does not exist'} in the account."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in is_existing_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "exists": False, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in is_existing_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "exists": False, "error": str(e), "message": str(e)}


def get_role(role_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed definition for a specific role.

    Args:
        role_name: Snowflake role name
        tool_context: ADK tool context

    Returns:
        Dictionary with role definition records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_role called for '%s'", role_name)
    try:
        session = _get_session(tool_context)
        inspector = Roles(session)
        records = inspector.get_role(role_name)
        return {
            "role_name": role_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} record(s) for role '{role_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_roles_by_owner(owner_name: str, tool_context: ToolContext) -> dict:
    """
    Get all roles owned by a specific owner.

    Args:
        owner_name: Name of the role owner
        tool_context: ADK tool context

    Returns:
        Dictionary with role records owned by the specified owner
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_roles_by_owner called for '%s'", owner_name)
    try:
        session = _get_session(tool_context)
        inspector = Roles(session)
        records = inspector.get_roles_by_owner(owner_name)
        return {
            "owner_name": owner_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} role(s) owned by '{owner_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_roles_by_owner for '%s': %s", owner_name, str(e))
        return {"owner_name": owner_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_roles_by_owner for '%s': %s", owner_name, str(e))
        return {"owner_name": owner_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_deleted_roles(tool_context: ToolContext) -> dict:
    """
    Get all deleted roles in the account.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with deleted role records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_deleted_roles called")
    try:
        session = _get_session(tool_context)
        inspector = Roles(session)
        records = inspector.get_deleted_roles()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} deleted role(s) in the account."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_deleted_roles: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_deleted_roles: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
