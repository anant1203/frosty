from src.infschema.replicationgroups import ReplicationGroups
from src.session import Session
from google.adk.tools import ToolContext
from snowflake.snowpark.functions import col
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


def list_replication_groups(tool_context: ToolContext) -> dict:
    """
    List all replication group at account level.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with list of replication group
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_replication_groups called")
    session = _get_session(tool_context)
    try:
        inspector = ReplicationGroups(session)
        df = session.table(inspector.col._view).select(
            col(inspector.col._replication_group_name)
        ).collect()
        group_list = [row[0] for row in df]
        return {
            "replication_groups": group_list,
            "count": len(group_list),
            "message": f"Found {len(group_list)} replication group(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_replication_groups: %s", str(e))
        return {"replication_groups": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_replication_groups: %s", str(e))
        return {"replication_groups": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}

def get_replication_group_properties(group_name: str, tool_context: ToolContext) -> dict:
    """
    Get properties of a specific replication group.

    Args:
        group_name: Name of the replication group
        tool_context: ADK tool context

    Returns:
        Dictionary with replication group properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_replication_group_properties called for '%s'", group_name)
    session = _get_session(tool_context)
    try:
        inspector = ReplicationGroups(session)
        if not inspector.is_existing_replication_group(group_name):
            return {"exists": False, "group_name": group_name.upper(), "message": f"Replication group '{group_name.upper()}' not found"}
        df = session.table(inspector.col._view).filter(
            col(inspector.col._replication_group_name) == group_name.upper()
        ).select(
            col(inspector.col._replication_group_id),
            col(inspector.col._replication_group_name),
            col(inspector.col._type),
            col(inspector.col._is_primary),
            col(inspector.col._is_snapshot),
            col(inspector.col._primary),
            col(inspector.col._replication_allowed_to_accounts),
            col(inspector.col._failover_allowed_to_accounts),
            col(inspector.col._object_types),
            col(inspector.col._secondary_state),
            col(inspector.col._created_on),
            col(inspector.col._next_scheduled_refresh),
            col(inspector.col._schedule),
            col(inspector.col._comment)
        ).collect()
        if df:
            row = df[0]
            return {
                "exists": True,
                "replication_group_id": row[0],
                "group_name": row[1],
                "type": row[2],
                "is_primary": row[3],
                "is_snapshot": row[4],
                "primary": row[5],
                "replication_allowed_to_accounts": row[6],
                "failover_allowed_to_accounts": row[7],
                "object_types": row[8],
                "secondary_state": row[9],
                "created_on": str(row[10]),
                "next_scheduled_refresh": str(row[11]),
                "schedule": row[12],
                "comment": row[13],
                "message": f"Retrieved properties for replication group '{group_name.upper()}'"
            }
        return {"exists": False, "group_name": group_name.upper(), "message": f"Replication group '{group_name.upper()}' not found"}
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_replication_group_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_replication_group_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}
