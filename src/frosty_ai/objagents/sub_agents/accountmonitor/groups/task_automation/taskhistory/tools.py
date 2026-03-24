import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.taskhistory import TaskHistory


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


def get_task_history_by_name(database_name: str, schema_name: str, task_name: str, tool_context: ToolContext) -> dict:
    """
    Get execution history for a specific task by its fully qualified name.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        task_name: Name of the task
        tool_context: ADK tool context

    Returns:
        Dictionary with task execution history records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_task_history_by_name called for '%s.%s.%s'", database_name, schema_name, task_name)
    try:
        session = _get_session(tool_context)
        inspector = TaskHistory(session)
        records = inspector.get_task_history_by_name(database_name, schema_name, task_name)
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "task_name": task_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} execution(s) for task '{database_name.upper()}.{schema_name.upper()}.{task_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_task_history_by_name: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_task_history_by_name: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_failed_tasks(tool_context: ToolContext) -> dict:
    """
    Get all task executions that failed.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with failed task execution records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_failed_tasks called")
    try:
        session = _get_session(tool_context)
        inspector = TaskHistory(session)
        records = inspector.get_failed_tasks()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} failed task execution(s)."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_failed_tasks: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_failed_tasks: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_task_history_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get task execution history within a specified time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with task execution records in the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_task_history_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = TaskHistory(session)
        records = inspector.get_task_history_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} task execution(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_task_history_in_time_range: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_task_history_in_time_range: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_task_history_by_state(state: str, tool_context: ToolContext) -> dict:
    """
    Get task execution history filtered by execution state.

    Args:
        state: Execution state to filter by (e.g. SUCCEEDED, FAILED, SKIPPED)
        tool_context: ADK tool context

    Returns:
        Dictionary with task execution records matching the specified state
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_task_history_by_state called for state '%s'", state)
    try:
        session = _get_session(tool_context)
        inspector = TaskHistory(session)
        records = inspector.get_task_history_by_state(state)
        return {
            "state": state.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} task execution(s) with state '{state.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_task_history_by_state: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_task_history_by_state: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_task_history_by_schema(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Get task execution history for all tasks within a specific schema.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with task execution records for the schema
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_task_history_by_schema called for '%s.%s'", database_name, schema_name)
    try:
        session = _get_session(tool_context)
        inspector = TaskHistory(session)
        records = inspector.get_task_history_by_schema(database_name, schema_name)
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} task execution(s) in schema '{database_name.upper()}.{schema_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_task_history_by_schema: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_task_history_by_schema: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}


def get_most_recent_run(database_name: str, schema_name: str, task_name: str, tool_context: ToolContext) -> dict:
    """
    Get the most recent execution record for a specific task.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        task_name: Name of the task
        tool_context: ADK tool context

    Returns:
        Dictionary with the most recent execution record for the task
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_most_recent_run called for '%s.%s.%s'", database_name, schema_name, task_name)
    try:
        session = _get_session(tool_context)
        inspector = TaskHistory(session)
        records = inspector.get_most_recent_run(database_name, schema_name, task_name)
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "task_name": task_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} most recent run record(s) for task '{database_name.upper()}.{schema_name.upper()}.{task_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_most_recent_run: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_most_recent_run: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}
