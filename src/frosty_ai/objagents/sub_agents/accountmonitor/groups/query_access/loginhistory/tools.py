import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.loginhistory import LoginHistory


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


def get_logins_by_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get login history for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with login records for the user
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_logins_by_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = LoginHistory(session)
        records = inspector.get_logins_by_user(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} login record(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_logins_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_logins_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_failed_logins(tool_context: ToolContext) -> dict:
    """
    Get all failed login attempts across the account.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with failed login records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_failed_logins called")
    try:
        session = _get_session(tool_context)
        inspector = LoginHistory(session)
        records = inspector.get_failed_logins()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} failed login attempt(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_failed_logins: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_failed_logins: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def get_failed_logins_by_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get all failed login attempts for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with failed login records for the user
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_failed_logins_by_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = LoginHistory(session)
        records = inspector.get_failed_logins_by_user(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} failed login attempt(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_failed_logins_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_failed_logins_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_logins_by_client_ip(client_ip: str, tool_context: ToolContext) -> dict:
    """
    Get login history originating from a specific client IP address.

    Args:
        client_ip: Client IP address
        tool_context: ADK tool context

    Returns:
        Dictionary with login records from the client IP
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_logins_by_client_ip called for '%s'", client_ip)
    try:
        session = _get_session(tool_context)
        inspector = LoginHistory(session)
        records = inspector.get_logins_by_client_ip(client_ip)
        return {
            "client_ip": client_ip,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} login record(s) from client IP '{client_ip}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_logins_by_client_ip: %s", str(e))
        return {"client_ip": client_ip, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_logins_by_client_ip: %s", str(e))
        return {"client_ip": client_ip, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_logins_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get login history within a specific time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with login records within the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_logins_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = LoginHistory(session)
        records = inspector.get_logins_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} login record(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_logins_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_logins_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_logins_by_client_type(client_type: str, tool_context: ToolContext) -> dict:
    """
    Get login history filtered by client type.

    Args:
        client_type: Type of client (e.g. 'PYTHON_CONNECTOR', 'JDBC_DRIVER', 'SNOWFLAKE_UI')
        tool_context: ADK tool context

    Returns:
        Dictionary with login records for the specified client type
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_logins_by_client_type called for '%s'", client_type)
    try:
        session = _get_session(tool_context)
        inspector = LoginHistory(session)
        records = inspector.get_logins_by_client_type(client_type)
        return {
            "client_type": client_type.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} login record(s) for client type '{client_type.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_logins_by_client_type: %s", str(e))
        return {"client_type": client_type.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_logins_by_client_type: %s", str(e))
        return {"client_type": client_type.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
