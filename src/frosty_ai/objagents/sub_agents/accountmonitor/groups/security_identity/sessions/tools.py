import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.sessions import Sessions


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


def get_sessions_by_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get session history for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with session records for the user
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_sessions_by_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = Sessions(session)
        records = inspector.get_sessions_by_user(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} session(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_sessions_by_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_sessions_by_user for '%s': %s", user_name, str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_sessions_by_client_application(client_application: str, tool_context: ToolContext) -> dict:
    """
    Get session history filtered by client application name.

    Args:
        client_application: Name of the client application
        tool_context: ADK tool context

    Returns:
        Dictionary with session records for the specified client application
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_sessions_by_client_application called for '%s'", client_application)
    try:
        session = _get_session(tool_context)
        inspector = Sessions(session)
        records = inspector.get_sessions_by_client_application(client_application)
        return {
            "client_application": client_application,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} session(s) for client application '{client_application}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_sessions_by_client_application for '%s': %s", client_application, str(e))
        return {"client_application": client_application, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_sessions_by_client_application for '%s': %s", client_application, str(e))
        return {"client_application": client_application, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_sessions_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get sessions that occurred within a specified time range.

    Args:
        start_time: Start of the time range (e.g. '2024-01-01 00:00:00')
        end_time: End of the time range (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with session records within the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_sessions_in_time_range called for '%s' to '%s'", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = Sessions(session)
        records = inspector.get_sessions_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} session(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_sessions_in_time_range for '%s' to '%s': %s", start_time, end_time, str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_sessions_in_time_range for '%s' to '%s': %s", start_time, end_time, str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_sessions_by_authentication_method(authentication_method: str, tool_context: ToolContext) -> dict:
    """
    Get session history filtered by authentication method.

    Args:
        authentication_method: Authentication method (e.g. PASSWORD, OAUTH, SAML)
        tool_context: ADK tool context

    Returns:
        Dictionary with session records for the specified authentication method
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_sessions_by_authentication_method called for '%s'", authentication_method)
    try:
        session = _get_session(tool_context)
        inspector = Sessions(session)
        records = inspector.get_sessions_by_authentication_method(authentication_method)
        return {
            "authentication_method": authentication_method.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} session(s) with authentication method '{authentication_method.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_sessions_by_authentication_method for '%s': %s", authentication_method, str(e))
        return {"authentication_method": authentication_method.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_sessions_by_authentication_method for '%s': %s", authentication_method, str(e))
        return {"authentication_method": authentication_method.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_session_by_id(session_id: str, tool_context: ToolContext) -> dict:
    """
    Get details for a specific session by its session ID.

    Args:
        session_id: Unique session identifier
        tool_context: ADK tool context

    Returns:
        Dictionary with session record for the given session ID
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_session_by_id called for '%s'", session_id)
    try:
        session = _get_session(tool_context)
        inspector = Sessions(session)
        records = inspector.get_session_by_id(session_id)
        return {
            "session_id": session_id,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} record(s) for session ID '{session_id}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_session_by_id for '%s': %s", session_id, str(e))
        return {"session_id": session_id, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_session_by_id for '%s': %s", session_id, str(e))
        return {"session_id": session_id, "records": [], "count": None, "error": str(e), "message": str(e)}
