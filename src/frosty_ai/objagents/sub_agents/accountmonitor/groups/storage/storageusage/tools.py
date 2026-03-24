import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.storageusage import StorageUsage


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


def get_storage_usage_in_time_range(start_date: str, end_date: str, tool_context: ToolContext) -> dict:
    """
    Get account-level storage usage records within a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        tool_context: ADK tool context

    Returns:
        Dictionary with storage usage records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_storage_usage_in_time_range called for %s to %s", start_date, end_date)
    try:
        session = _get_session(tool_context)
        inspector = StorageUsage(session)
        records = inspector.get_storage_usage_in_time_range(start_date, end_date)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} storage usage record(s) between {start_date} and {end_date}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_storage_usage_in_time_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_storage_usage_in_time_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}


def get_latest_storage_usage(tool_context: ToolContext) -> dict:
    """
    Get the most recent account-level storage usage snapshot.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with the latest storage usage record(s)
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_latest_storage_usage called")
    try:
        session = _get_session(tool_context)
        inspector = StorageUsage(session)
        records = inspector.get_latest_storage_usage()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Latest storage usage snapshot: {len(records)} record(s) returned."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_latest_storage_usage: %s", str(e))
        return {"error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_latest_storage_usage: %s", str(e))
        return {"error": str(e), "message": str(e)}


def get_average_database_bytes_in_range(start_date: str, end_date: str, tool_context: ToolContext) -> dict:
    """
    Get the average database bytes consumed within a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        tool_context: ADK tool context

    Returns:
        Dictionary with the average database bytes and supporting records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_average_database_bytes_in_range called for %s to %s", start_date, end_date)
    try:
        session = _get_session(tool_context)
        inspector = StorageUsage(session)
        records = inspector.get_average_database_bytes_in_range(start_date, end_date)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Average database bytes in range {start_date} to {end_date}: {len(records)} record(s) returned."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_average_database_bytes_in_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_average_database_bytes_in_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}


def get_all_storage_usage(tool_context: ToolContext) -> dict:
    """
    Get the full account-level storage usage history.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with all storage usage records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_all_storage_usage called")
    try:
        session = _get_session(tool_context)
        inspector = StorageUsage(session)
        records = inspector.get_all_storage_usage()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Retrieved full storage usage history: {len(records)} record(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_all_storage_usage: %s", str(e))
        return {"error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_all_storage_usage: %s", str(e))
        return {"error": str(e), "message": str(e)}
