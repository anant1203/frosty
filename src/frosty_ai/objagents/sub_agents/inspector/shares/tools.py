from src.infschema.shares import Shares
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


def list_all_shares(tool_context: ToolContext) -> dict:
    """
    List all share at account level.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with list of share
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_shares called")
    session = _get_session(tool_context)
    try:
        inspector = Shares(session)
        df = session.table(inspector.col._view).select(
            col(inspector.col._share_name)
        ).collect()
        share_list = [row[0] for row in df]
        return {
            "shares": share_list,
            "count": len(share_list),
            "message": f"Found {len(share_list)} share(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_all_shares: %s", str(e))
        return {"shares": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_all_shares: %s", str(e))
        return {"shares": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}

def get_share_properties(share_name: str, tool_context: ToolContext) -> dict:
    """
    Get properties of a specific share.

    Args:
        share_name: Name of the share
        tool_context: ADK tool context

    Returns:
        Dictionary with share properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_share_properties called for '%s'", share_name)
    session = _get_session(tool_context)
    try:
        inspector = Shares(session)
        if not inspector.is_existing_share(share_name):
            return {"exists": False, "share_name": share_name.upper(), "message": f"Share '{share_name.upper()}' not found"}
        df = session.table(inspector.col._view).filter(
            col(inspector.col._share_name) == share_name.upper()
        ).select(
            col(inspector.col._share_name),
            col(inspector.col._share_owner),
            col(inspector.col._comment),
            col(inspector.col._listing_global_name),
            col(inspector.col._created_on),
            col(inspector.col._kind),
            col(inspector.col._consumer_accounts)
        ).collect()
        if df:
            row = df[0]
            return {
                "exists": True,
                "share_name": row[0],
                "owner": row[1],
                "comment": row[2],
                "listing_global_name": row[3],
                "created_on": str(row[4]),
                "kind": row[5],
                "consumer_accounts": row[6],
                "message": f"Retrieved properties for share '{share_name.upper()}'"
            }
        return {"exists": False, "share_name": share_name.upper(), "message": f"Share '{share_name.upper()}' not found"}
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_share_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_share_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}
