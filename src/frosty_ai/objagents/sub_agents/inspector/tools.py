import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../../'))
import logging
from google.adk.tools import ToolContext


def get_created_objects_from_memory(tool_context: ToolContext) -> dict:
    """
    Retrieve all successfully created Snowflake objects from the session state.

    This tool reads app:TASKS_PERFORMED from the session state to find all objects
    that were successfully created in the current session. It filters for entries
    with OPERATION_STATUS: SUCCESS and returns the matching list.

    Args:
        tool_context: ADK tool context containing state information

    Returns:
        List of successfully created objects recorded in the session state
    """
    try:
        logger_name = tool_context.state.get("app:LOGGER")
        logger = logging.getLogger(logger_name).getChild(__name__)
        logger.debug("INSIDE TO FETCH MEMORIES")
        tasks = tool_context.state.get("app:TASKS_PERFORMED", [])
        results = [t for t in tasks if isinstance(t, dict) and t.get("OPERATION_STATUS") == "SUCCESS"]
        return results
    except Exception as e:
        logger.error(f"Error retrieving memories: {str(e)}")
        return {
            "success": False,
            "objects": [],
            "count": 0,
            "error": str(e),
            "message": f"Error retrieving created objects from session state: {str(e)}"
        }


def get_successful_operations(tool_context: ToolContext) -> dict:
    """
    Retrieve all successfully created Snowflake objects from the current session state.

    This tool reads app:TASKS_PERFORMED from the session state and returns all entries
    with OPERATION_STATUS: SUCCESS. The caller should inspect the returned list and
    deduce which object types were created from the OBJECT_IDENTIFIER and
    GENERATED_QUERY fields. Use this to understand what was built in the current session
    when the full history is needed (e.g., for role planning, governance sweeps, or
    session reconciliation).

    Note: For live Snowflake objects not created in this session (e.g., existing roles),
    delegate to the appropriate inspector sub-agent or pillar agent.

    Args:
        tool_context: ADK tool context containing state information

    Returns:
        List of all successfully created objects recorded in the current session state
    """
    try:
        logger_name = tool_context.state.get("app:LOGGER")
        logger = logging.getLogger(logger_name).getChild(__name__)
        logger.debug("INSIDE TO FETCH SESSION OPERATIONS")
        tasks = tool_context.state.get("app:TASKS_PERFORMED", [])
        results = [t for t in tasks if isinstance(t, dict) and t.get("OPERATION_STATUS") == "SUCCESS"]
        return results
    except Exception as e:
        logger.error(f"Error retrieving session operations: {str(e)}")
        return {
            "success": False,
            "objects": [],
            "count": 0,
            "error": str(e),
            "message": f"Error retrieving objects from session state: {str(e)}"
        }
