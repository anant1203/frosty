from src.infschema.queryaccelerationhistory import QueryAccelerationHistory
from src.session import Session
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
import logging

def _get_session(tool_context: ToolContext):
    """Helper function to get Snowflake session from tool context."""
    session_inst = Session()
    username = tool_context.state.get('user:SNOWFLAKE_USER_NAME')
    account = tool_context.state.get('app:ACCOUNT_IDENTIFIER')
    session_inst.set_user(username)
    session_inst.set_account(account)
    session_inst.set_password(tool_context.state.get('user:USER_PASSWORD'))
    if tool_context.state.get('user:AUTHENTICATOR'):
        session_inst.set_authenticator(tool_context.state.get('user:AUTHENTICATOR'))
    if tool_context.state.get('user:ROLE'):
        session_inst.set_role(tool_context.state.get('user:ROLE'))
    if tool_context.state.get('app:WAREHOUSE'):
        session_inst.set_warehouse(tool_context.state.get('app:WAREHOUSE'))
    if tool_context.state.get('app:DATABASE'):
        session_inst.set_database(tool_context.state.get('app:DATABASE'))
    session = session_inst.get_session()
    return session


def get_query_acceleration_history(database_name: str, tool_context: ToolContext, result_limit: int = 100) -> dict:
    """
    Get query acceleration history data.

    Args:
        database_name: Name of the database
        result_limit: Maximum number of records to return
        tool_context: ADK tool context

    Returns:
        Dictionary with query acceleration history records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_query_acceleration_history called for database '%s'", database_name)
    session = _get_session(tool_context)
    try:
        inspector = QueryAccelerationHistory(session)
        df = inspector.get_history(database_name, result_limit)
        records = [row.as_dict() for row in df]
        return {
            "database_name": database_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} query acceleration history record(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_query_acceleration_history: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_query_acceleration_history: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}
