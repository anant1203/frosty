import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.users import Users


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


def get_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed definition for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with user definition records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        records = inspector.get_user(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} record(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_all_active_users(tool_context: ToolContext) -> dict:
    """
    Get all active (non-deleted, non-disabled) users in the account.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with all active user records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_all_active_users called")
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        records = inspector.get_all_active_users()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} active user(s) in the account."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_all_active_users: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_all_active_users: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def get_disabled_users(tool_context: ToolContext) -> dict:
    """
    Get all disabled users in the account.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with disabled user records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_disabled_users called")
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        records = inspector.get_disabled_users()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} disabled user(s) in the account."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_disabled_users: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_disabled_users: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def is_existing_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Check whether a user exists in the account.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with an exists boolean and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("is_existing_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        exists = inspector.is_existing_user(user_name)
        return {
            "user_name": user_name.upper(),
            "exists": exists,
            "message": f"User '{user_name.upper()}' {'exists' if exists else 'does not exist'} in the account."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in is_existing_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "exists": False, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in is_existing_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "exists": False, "error": str(e), "message": str(e)}


def get_users_by_default_role(role_name: str, tool_context: ToolContext) -> dict:
    """
    Get all users whose default role is the specified role.

    Args:
        role_name: Snowflake role name
        tool_context: ADK tool context

    Returns:
        Dictionary with user records that have the specified default role
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_users_by_default_role called for '%s'", role_name)
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        records = inspector.get_users_by_default_role(role_name)
        return {
            "role_name": role_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} user(s) with default role '{role_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_users_by_default_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_users_by_default_role for '%s': %s", role_name, str(e))
        return {"role_name": role_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_users_by_default_warehouse(warehouse_name: str, tool_context: ToolContext) -> dict:
    """
    Get all users whose default warehouse is the specified warehouse.

    Args:
        warehouse_name: Snowflake warehouse name
        tool_context: ADK tool context

    Returns:
        Dictionary with user records that have the specified default warehouse
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_users_by_default_warehouse called for '%s'", warehouse_name)
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        records = inspector.get_users_by_default_warehouse(warehouse_name)
        return {
            "warehouse_name": warehouse_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} user(s) with default warehouse '{warehouse_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_users_by_default_warehouse for '%s': %s", warehouse_name, str(e))
        return {"warehouse_name": warehouse_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_users_by_default_warehouse for '%s': %s", warehouse_name, str(e))
        return {"warehouse_name": warehouse_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_users_not_logged_in_since(since_timestamp: str, tool_context: ToolContext) -> dict:
    """
    Get users who have not logged in since the specified timestamp.

    Args:
        since_timestamp: Timestamp threshold (e.g. '2024-01-01 00:00:00')
        tool_context: ADK tool context

    Returns:
        Dictionary with user records that have not logged in since the given timestamp
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_users_not_logged_in_since called for '%s'", since_timestamp)
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        records = inspector.get_users_not_logged_in_since(since_timestamp)
        return {
            "since_timestamp": since_timestamp,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} user(s) who have not logged in since {since_timestamp}."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_users_not_logged_in_since for '%s': %s", since_timestamp, str(e))
        return {"since_timestamp": since_timestamp, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_users_not_logged_in_since for '%s': %s", since_timestamp, str(e))
        return {"since_timestamp": since_timestamp, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_user_last_login(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get the last login time for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with the user's last login information
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_user_last_login called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = Users(session)
        records = inspector.get_user_last_login(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} last login record(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_user_last_login for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_user_last_login for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
