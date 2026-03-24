import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.loadhistory import LoadHistory


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


def get_load_history_for_table(catalog_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get data load history for a specific table.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context

    Returns:
        Dictionary with load history records for the table
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_load_history_for_table called for '%s.%s.%s'", catalog_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        inspector = LoadHistory(session)
        records = inspector.get_load_history_for_table(catalog_name, schema_name, table_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} load history record(s) for '{catalog_name.upper()}.{schema_name.upper()}.{table_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_load_history_for_table: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_load_history_for_table: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_failed_loads(tool_context: ToolContext) -> dict:
    """
    Get all failed data load operations across the account.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with failed load records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_failed_loads called")
    try:
        session = _get_session(tool_context)
        inspector = LoadHistory(session)
        records = inspector.get_failed_loads()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} failed load operation(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_failed_loads: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_failed_loads: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def get_load_history_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get data load history within a specific time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with load history records within the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_load_history_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = LoadHistory(session)
        records = inspector.get_load_history_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} load history record(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_load_history_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_load_history_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "records": [], "count": None, "error": str(e), "message": str(e)}


def get_load_history_by_pipe(pipe_catalog_name: str, pipe_schema_name: str, pipe_name: str, tool_context: ToolContext) -> dict:
    """
    Get data load history for a specific pipe.

    Args:
        pipe_catalog_name: Name of the database (catalog) containing the pipe
        pipe_schema_name: Name of the schema containing the pipe
        pipe_name: Name of the pipe
        tool_context: ADK tool context

    Returns:
        Dictionary with load history records for the pipe
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_load_history_by_pipe called for '%s.%s.%s'", pipe_catalog_name, pipe_schema_name, pipe_name)
    try:
        session = _get_session(tool_context)
        inspector = LoadHistory(session)
        records = inspector.get_load_history_by_pipe(pipe_catalog_name, pipe_schema_name, pipe_name)
        return {
            "pipe_catalog_name": pipe_catalog_name.upper(),
            "pipe_schema_name": pipe_schema_name.upper(),
            "pipe_name": pipe_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} load history record(s) for pipe '{pipe_catalog_name.upper()}.{pipe_schema_name.upper()}.{pipe_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_load_history_by_pipe: %s", str(e))
        return {"pipe_catalog_name": pipe_catalog_name.upper(), "pipe_schema_name": pipe_schema_name.upper(), "pipe_name": pipe_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_load_history_by_pipe: %s", str(e))
        return {"pipe_catalog_name": pipe_catalog_name.upper(), "pipe_schema_name": pipe_schema_name.upper(), "pipe_name": pipe_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_load_errors_for_table(catalog_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get data load error records for a specific table.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context

    Returns:
        Dictionary with load error records for the table
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_load_errors_for_table called for '%s.%s.%s'", catalog_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        inspector = LoadHistory(session)
        records = inspector.get_load_errors_for_table(catalog_name, schema_name, table_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} load error(s) for '{catalog_name.upper()}.{schema_name.upper()}.{table_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_load_errors_for_table: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_load_errors_for_table: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
