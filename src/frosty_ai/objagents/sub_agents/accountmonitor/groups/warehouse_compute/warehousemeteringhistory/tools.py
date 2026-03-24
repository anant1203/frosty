import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.warehousemeteringhistory import WarehouseMeteringHistory


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


def get_metering_by_warehouse(warehouse_name: str, tool_context: ToolContext) -> dict:
    """
    Get warehouse metering history records for a specific warehouse.

    Args:
        warehouse_name: Name of the warehouse
        tool_context: ADK tool context

    Returns:
        Dictionary with metering records for the warehouse
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_metering_by_warehouse called for '%s'", warehouse_name)
    try:
        session = _get_session(tool_context)
        inspector = WarehouseMeteringHistory(session)
        records = inspector.get_metering_by_warehouse(warehouse_name)
        return {
            "warehouse_name": warehouse_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} metering record(s) for warehouse '{warehouse_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_metering_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_metering_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "error": str(e), "message": str(e)}


def get_metering_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get warehouse metering history records within a time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with metering records in the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_metering_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = WarehouseMeteringHistory(session)
        records = inspector.get_metering_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} metering record(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_metering_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_metering_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}


def get_total_credits_by_warehouse(warehouse_name: str, tool_context: ToolContext) -> dict:
    """
    Get total credits consumed by a specific warehouse.

    Args:
        warehouse_name: Name of the warehouse
        tool_context: ADK tool context

    Returns:
        Dictionary with total credits used by the warehouse
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_total_credits_by_warehouse called for '%s'", warehouse_name)
    try:
        session = _get_session(tool_context)
        inspector = WarehouseMeteringHistory(session)
        records = inspector.get_total_credits_by_warehouse(warehouse_name)
        return {
            "warehouse_name": warehouse_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Total credits for warehouse '{warehouse_name.upper()}': {len(records)} record(s) returned."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_total_credits_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_total_credits_by_warehouse: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "error": str(e), "message": str(e)}


def get_all_warehouse_names(tool_context: ToolContext) -> dict:
    """
    Get a list of all warehouse names that appear in metering history.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with list of warehouse names
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_all_warehouse_names called")
    try:
        session = _get_session(tool_context)
        inspector = WarehouseMeteringHistory(session)
        records = inspector.get_all_warehouse_names()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} warehouse name(s) in metering history."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_all_warehouse_names: %s", str(e))
        return {"error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_all_warehouse_names: %s", str(e))
        return {"error": str(e), "message": str(e)}


def get_credits_by_warehouse_in_time_range(warehouse_name: str, start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get credits consumed by a specific warehouse within a time range.

    Args:
        warehouse_name: Name of the warehouse
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with metering records for the warehouse in the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_credits_by_warehouse_in_time_range called for '%s' from %s to %s", warehouse_name, start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = WarehouseMeteringHistory(session)
        records = inspector.get_credits_by_warehouse_in_time_range(warehouse_name, start_time, end_time)
        return {
            "warehouse_name": warehouse_name.upper(),
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} metering record(s) for warehouse '{warehouse_name.upper()}' between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_credits_by_warehouse_in_time_range: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_credits_by_warehouse_in_time_range: %s", str(e))
        return {"warehouse_name": warehouse_name.upper(), "start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}
