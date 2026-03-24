import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.queryhistory import QueryHistory


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


def get_queries_by_user(user_name: str, tool_context: ToolContext, start_time: str = None, end_time: str = None) -> dict:
    """
    Get query execution history for a specific user, with optional time range.

    Args:
        user_name: Snowflake username
        start_time: Optional start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: Optional end timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with query records for the user
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_queries_by_user called for '%s', range '%s' to '%s'", user_name, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_queries_by_user(user_name, start_time, end_time)
        time_range_msg = f" between {start_time} and {end_time}" if start_time and end_time else ""
        return {
            "user_name": user_name.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} query/queries for user '{user_name.upper()}'{time_range_msg}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_queries_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_queries_by_user: %s", str(e))
        return {"user_name": user_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_queries_by_warehouse(warehouse_name: str, tool_context: ToolContext, start_time: str = None, end_time: str = None) -> dict:
    """
    Get query execution history for a specific warehouse, with optional time range.

    Args:
        warehouse_name: Name of the warehouse
        start_time: Optional start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: Optional end timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with query records for the warehouse
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_queries_by_warehouse called for '%s', range '%s' to '%s'", warehouse_name, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_queries_by_warehouse(warehouse_name, start_time, end_time)
        time_range_msg = f" between {start_time} and {end_time}" if start_time and end_time else ""
        return {
            "warehouse_name": warehouse_name.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} query/queries for warehouse '{warehouse_name.upper()}'{time_range_msg}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_queries_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_queries_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_failed_queries(tool_context: ToolContext, start_time: str = None, end_time: str = None) -> dict:
    """
    Get all queries that failed execution, with optional time range.

    Args:
        start_time: Optional start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: Optional end timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with failed query records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_failed_queries called, range '%s' to '%s'", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_failed_queries(start_time, end_time)
        time_range_msg = f" between {start_time} and {end_time}" if start_time and end_time else ""
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} failed query/queries{time_range_msg}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_failed_queries: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_failed_queries: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def get_queries_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get queries executed within a specific time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with query records within the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_queries_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_queries_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} query/queries between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_queries_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_queries_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_long_running_queries(min_elapsed_ms: int, tool_context: ToolContext, start_time: str = None, end_time: str = None) -> dict:
    """
    Get queries that took longer than the specified duration, with optional time range.

    Args:
        min_elapsed_ms: Minimum elapsed time in milliseconds
        start_time: Optional start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: Optional end timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with long-running query records sorted by elapsed time descending
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_long_running_queries called with min_elapsed_ms=%d, range '%s' to '%s'", min_elapsed_ms, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_long_running_queries(min_elapsed_ms, start_time, end_time)
        time_range_msg = f" between {start_time} and {end_time}" if start_time and end_time else ""
        return {
            "min_elapsed_ms": min_elapsed_ms,
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} query/queries running longer than {min_elapsed_ms}ms{time_range_msg}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_long_running_queries: %s", str(e))
        return {"min_elapsed_ms": min_elapsed_ms, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_long_running_queries: %s", str(e))
        return {"min_elapsed_ms": min_elapsed_ms, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_queries_by_type(query_type: str, tool_context: ToolContext, start_time: str = None, end_time: str = None) -> dict:
    """
    Get query execution history filtered by query type, with optional time range.

    Args:
        query_type: Type of query (e.g. 'SELECT', 'INSERT', 'UPDATE', 'DELETE')
        start_time: Optional start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: Optional end timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with query records for the specified type
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_queries_by_type called for '%s', range '%s' to '%s'", query_type, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_queries_by_type(query_type, start_time, end_time)
        time_range_msg = f" between {start_time} and {end_time}" if start_time and end_time else ""
        return {
            "query_type": query_type.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} query/queries of type '{query_type.upper()}'{time_range_msg}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_queries_by_type: %s", str(e))
        return {"query_type": query_type.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_queries_by_type: %s", str(e))
        return {"query_type": query_type.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_queries_by_database(database_name: str, tool_context: ToolContext, start_time: str = None, end_time: str = None) -> dict:
    """
    Get query execution history for a specific database, with optional time range.

    Args:
        database_name: Name of the database
        start_time: Optional start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: Optional end timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with query records for the database
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_queries_by_database called for '%s', range '%s' to '%s'", database_name, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_queries_by_database(database_name, start_time, end_time)
        time_range_msg = f" between {start_time} and {end_time}" if start_time and end_time else ""
        return {
            "database_name": database_name.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} query/queries for database '{database_name.upper()}'{time_range_msg}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_queries_by_database: %s", str(e))
        return {"database_name": database_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_queries_by_database: %s", str(e))
        return {"database_name": database_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_credits_by_warehouse(warehouse_name: str, tool_context: ToolContext, start_time: str = None, end_time: str = None) -> dict:
    """
    Get credit usage attributed to a specific warehouse from query history, with optional time range.

    Args:
        warehouse_name: Name of the warehouse
        start_time: Optional start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: Optional end timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with credit usage records for the warehouse
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_credits_by_warehouse called for '%s', range '%s' to '%s'", warehouse_name, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = QueryHistory(session)
        records = inspector.get_credits_by_warehouse(warehouse_name, start_time, end_time)
        time_range_msg = f" between {start_time} and {end_time}" if start_time and end_time else ""
        return {
            "warehouse_name": warehouse_name.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} credit usage record(s) for warehouse '{warehouse_name.upper()}'{time_range_msg}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_credits_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_credits_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
