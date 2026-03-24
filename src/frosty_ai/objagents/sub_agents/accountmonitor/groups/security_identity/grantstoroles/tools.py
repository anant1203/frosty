import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.grantstoroles import GrantsToRoles


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


def get_grants_for_role(role_name: str, tool_context: ToolContext) -> dict:
    """
    Get all privilege grants for a specific role.

    Args:
        role_name: Snowflake role name
        tool_context: ADK tool context

    Returns:
        Dictionary with grant records for the role
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_grants_for_role called for '%s'", role_name)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToRoles(session)
        records = inspector.get_grants_for_role(role_name)
        return {
            "role_name": role_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} grant(s) for role '{role_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_grants_for_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_grants_for_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_grants_by_privilege(privilege: str, tool_context: ToolContext) -> dict:
    """
    Get all role grants filtered by a specific privilege type.

    Args:
        privilege: Snowflake privilege name (e.g. SELECT, INSERT, USAGE)
        tool_context: ADK tool context

    Returns:
        Dictionary with grant records for the privilege
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_grants_by_privilege called for '%s'", privilege)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToRoles(session)
        records = inspector.get_grants_by_privilege(privilege)
        return {
            "privilege": privilege.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} grant(s) with privilege '{privilege.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_grants_by_privilege for '%s': %s", privilege, str(e))
        return {"privilege": privilege.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_grants_by_privilege for '%s': %s", privilege, str(e))
        return {"privilege": privilege.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_grants_on_object(granted_on: str, object_name: str, tool_context: ToolContext) -> dict:
    """
    Get all role grants on a specific object.

    Args:
        granted_on: Object type (e.g. TABLE, SCHEMA, DATABASE)
        object_name: Name of the object
        tool_context: ADK tool context

    Returns:
        Dictionary with grant records on the specified object
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_grants_on_object called for '%s' '%s'", granted_on, object_name)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToRoles(session)
        records = inspector.get_grants_on_object(granted_on, object_name)
        return {
            "granted_on": granted_on.upper(),
            "object_name": object_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} grant(s) on {granted_on.upper()} '{object_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_grants_on_object for '%s' '%s': %s", granted_on, object_name, str(e))
        return {"granted_on": granted_on.upper(), "object_name": object_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_grants_on_object for '%s' '%s': %s", granted_on, object_name, str(e))
        return {"granted_on": granted_on.upper(), "object_name": object_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_grants_with_grant_option(role_name: str, tool_context: ToolContext) -> dict:
    """
    Get all grants for a role that include the grant option (WITH GRANT OPTION).

    Args:
        role_name: Snowflake role name
        tool_context: ADK tool context

    Returns:
        Dictionary with grant records that have grant option enabled
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_grants_with_grant_option called for '%s'", role_name)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToRoles(session)
        records = inspector.get_grants_with_grant_option(role_name)
        return {
            "role_name": role_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} grant(s) with grant option for role '{role_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_grants_with_grant_option for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_grants_with_grant_option for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_active_grants_for_role(role_name: str, tool_context: ToolContext) -> dict:
    """
    Get all active (non-deleted) privilege grants for a specific role.

    Args:
        role_name: Snowflake role name
        tool_context: ADK tool context

    Returns:
        Dictionary with active grant records for the role
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_active_grants_for_role called for '%s'", role_name)
    try:
        session = _get_session(tool_context)
        inspector = GrantsToRoles(session)
        records = inspector.get_active_grants_for_role(role_name)
        return {
            "role_name": role_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} active grant(s) for role '{role_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_active_grants_for_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_active_grants_for_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_grants_by_grantor(granted_by: str, tool_context: ToolContext) -> dict:
    """
    Get all role grants issued by a specific grantor.

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
        inspector = GrantsToRoles(session)
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
