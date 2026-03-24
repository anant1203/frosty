import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.datatransferhistory import DataTransferHistory


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


def get_transfers_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get data transfer records within a time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with data transfer records in the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_transfers_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = DataTransferHistory(session)
        records = inspector.get_transfers_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} data transfer record(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_transfers_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_transfers_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}


def get_transfers_by_source_cloud(source_cloud: str, tool_context: ToolContext) -> dict:
    """
    Get data transfer records filtered by source cloud provider.

    Args:
        source_cloud: Source cloud provider name (e.g. 'AWS', 'AZURE', 'GCP')
        tool_context: ADK tool context

    Returns:
        Dictionary with transfer records from the source cloud
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_transfers_by_source_cloud called for '%s'", source_cloud)
    try:
        session = _get_session(tool_context)
        inspector = DataTransferHistory(session)
        records = inspector.get_transfers_by_source_cloud(source_cloud)
        return {
            "source_cloud": source_cloud.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} data transfer record(s) from source cloud '{source_cloud.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_transfers_by_source_cloud: %s", str(e))
        return {"source_cloud": source_cloud.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_transfers_by_source_cloud: %s", str(e))
        return {"source_cloud": source_cloud.upper(), "error": str(e), "message": str(e)}


def get_transfers_by_target_cloud(target_cloud: str, tool_context: ToolContext) -> dict:
    """
    Get data transfer records filtered by target cloud provider.

    Args:
        target_cloud: Target cloud provider name (e.g. 'AWS', 'AZURE', 'GCP')
        tool_context: ADK tool context

    Returns:
        Dictionary with transfer records to the target cloud
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_transfers_by_target_cloud called for '%s'", target_cloud)
    try:
        session = _get_session(tool_context)
        inspector = DataTransferHistory(session)
        records = inspector.get_transfers_by_target_cloud(target_cloud)
        return {
            "target_cloud": target_cloud.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} data transfer record(s) to target cloud '{target_cloud.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_transfers_by_target_cloud: %s", str(e))
        return {"target_cloud": target_cloud.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_transfers_by_target_cloud: %s", str(e))
        return {"target_cloud": target_cloud.upper(), "error": str(e), "message": str(e)}


def get_transfers_by_type(transfer_type: str, tool_context: ToolContext) -> dict:
    """
    Get data transfer records filtered by transfer type.

    Args:
        transfer_type: The type of data transfer to filter by
        tool_context: ADK tool context

    Returns:
        Dictionary with transfer records of the specified type
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_transfers_by_type called for '%s'", transfer_type)
    try:
        session = _get_session(tool_context)
        inspector = DataTransferHistory(session)
        records = inspector.get_transfers_by_type(transfer_type)
        return {
            "transfer_type": transfer_type.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} data transfer record(s) of type '{transfer_type.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_transfers_by_type: %s", str(e))
        return {"transfer_type": transfer_type.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_transfers_by_type: %s", str(e))
        return {"transfer_type": transfer_type.upper(), "error": str(e), "message": str(e)}


def get_total_bytes_transferred_in_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get total bytes transferred in a time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with total bytes transferred in the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_total_bytes_transferred_in_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = DataTransferHistory(session)
        records = inspector.get_total_bytes_transferred_in_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Total bytes transferred from {start_time} to {end_time}: {len(records)} record(s) returned."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_total_bytes_transferred_in_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_total_bytes_transferred_in_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}
