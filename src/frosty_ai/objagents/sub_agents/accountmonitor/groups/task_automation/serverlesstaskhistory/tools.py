import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.serverlesstaskhistory import ServerlessTaskHistory


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


def get_history_for_task(database_name: str, schema_name: str, task_name: str, tool_context: ToolContext) -> dict:
    """
    Get serverless task execution history for a specific task.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        task_name: Name of the serverless task
        tool_context: ADK tool context

    Returns:
        Dictionary with serverless task execution history records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_history_for_task called for '%s.%s.%s'", database_name, schema_name, task_name)
    try:
        session = _get_session(tool_context)
        inspector = ServerlessTaskHistory(session)
        records = inspector.get_history_for_task(database_name, schema_name, task_name)
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "task_name": task_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} serverless task execution(s) for '{database_name.upper()}.{schema_name.upper()}.{task_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_history_for_task: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_history_for_task: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_history_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get serverless task execution history within a specified time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with serverless task execution records in the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_history_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = ServerlessTaskHistory(session)
        records = inspector.get_history_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} serverless task execution(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_history_in_time_range: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_history_in_time_range: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_total_credits_for_task(database_name: str, schema_name: str, task_name: str, tool_context: ToolContext) -> dict:
    """
    Get total credits consumed by a specific serverless task.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        task_name: Name of the serverless task
        tool_context: ADK tool context

    Returns:
        Dictionary with total credits consumed by the serverless task
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_total_credits_for_task called for '%s.%s.%s'", database_name, schema_name, task_name)
    try:
        session = _get_session(tool_context)
        inspector = ServerlessTaskHistory(session)
        records = inspector.get_total_credits_for_task(database_name, schema_name, task_name)
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "task_name": task_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} credit record(s) for serverless task '{database_name.upper()}.{schema_name.upper()}.{task_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_total_credits_for_task: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_total_credits_for_task: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_history_by_database(database_name: str, tool_context: ToolContext) -> dict:
    """
    Get serverless task execution history for all tasks in a specific database.

    Args:
        database_name: Name of the database
        tool_context: ADK tool context

    Returns:
        Dictionary with serverless task execution records for the database
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_history_by_database called for '%s'", database_name)
    try:
        session = _get_session(tool_context)
        inspector = ServerlessTaskHistory(session)
        records = inspector.get_history_by_database(database_name)
        return {
            "database_name": database_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} serverless task execution(s) in database '{database_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_history_by_database: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_history_by_database: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}
