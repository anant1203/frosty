import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.accesshistory import AccessHistory


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


def get_access_history_by_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Get data access history for a specific user.

    Args:
        user_name: Snowflake username
        tool_context: ADK tool context

    Returns:
        Dictionary with access history records for the user
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_access_history_by_user called for '%s'", user_name)
    try:
        session = _get_session(tool_context)
        inspector = AccessHistory(session)
        records = inspector.get_access_history_by_user(user_name)
        return {
            "user_name": user_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} access history record(s) for user '{user_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_access_history_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_access_history_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_access_history_by_query(query_id: str, tool_context: ToolContext) -> dict:
    """
    Get data access history for a specific query ID.

    Args:
        query_id: Snowflake query ID
        tool_context: ADK tool context

    Returns:
        Dictionary with access history records for the query
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_access_history_by_query called for '%s'", query_id)
    try:
        session = _get_session(tool_context)
        inspector = AccessHistory(session)
        records = inspector.get_access_history_by_query(query_id)
        return {
            "query_id": query_id,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} access history record(s) for query '{query_id}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_access_history_by_query: %s", str(e))
        return {"query_id": query_id, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_access_history_by_query: %s", str(e))
        return {"query_id": query_id, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_access_history_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get data access history within a specific time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with access history records within the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_access_history_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = AccessHistory(session)
        records = inspector.get_access_history_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} access history record(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_access_history_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_access_history_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_access_history_by_query_type(query_type: str, tool_context: ToolContext) -> dict:
    """
    Get data access history filtered by query type.

    Args:
        query_type: Type of query (e.g. 'SELECT', 'INSERT', 'UPDATE', 'DELETE')
        tool_context: ADK tool context

    Returns:
        Dictionary with access history records for the specified query type
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_access_history_by_query_type called for '%s'", query_type)
    try:
        session = _get_session(tool_context)
        inspector = AccessHistory(session)
        records = inspector.get_access_history_by_query_type(query_type)
        return {
            "query_type": query_type.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} access history record(s) for query type '{query_type.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_access_history_by_query_type: %s", str(e))
        return {"query_type": query_type.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_access_history_by_query_type: %s", str(e))
        return {"query_type": query_type.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_access_history_by_user_in_time_range(user_name: str, start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get data access history for a specific user within a time range.

    Args:
        user_name: Snowflake username
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with access history records for the user within the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_access_history_by_user_in_time_range called for '%s' from %s to %s", user_name, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = AccessHistory(session)
        records = inspector.get_access_history_by_user_in_time_range(user_name, start_time, end_time)
        return {
            "user_name": user_name.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} access history record(s) for user '{user_name.upper()}' between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_access_history_by_user_in_time_range: %s", str(e))
        return {"user_name": user_name.upper(), "start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_access_history_by_user_in_time_range: %s", str(e))
        return {"user_name": user_name.upper(), "start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}
