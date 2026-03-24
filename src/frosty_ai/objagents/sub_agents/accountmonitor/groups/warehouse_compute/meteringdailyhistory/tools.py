import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.meteringdailyhistory import MeteringDailyHistory


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


def get_metering_in_date_range(start_date: str, end_date: str, tool_context: ToolContext) -> dict:
    """
    Get daily metering history records within a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        tool_context: ADK tool context

    Returns:
        Dictionary with daily metering records in the date range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_metering_in_date_range called for %s to %s", start_date, end_date)
    try:
        session = _get_session(tool_context)
        inspector = MeteringDailyHistory(session)
        records = inspector.get_metering_in_date_range(start_date, end_date)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} daily metering record(s) between {start_date} and {end_date}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_metering_in_date_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_metering_in_date_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}


def get_metering_by_service_type(service_type: str, tool_context: ToolContext) -> dict:
    """
    Get daily metering history records for a specific service type.

    Args:
        service_type: The service type to filter by
        tool_context: ADK tool context

    Returns:
        Dictionary with metering records for the service type
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_metering_by_service_type called for '%s'", service_type)
    try:
        session = _get_session(tool_context)
        inspector = MeteringDailyHistory(session)
        records = inspector.get_metering_by_service_type(service_type)
        return {
            "service_type": service_type.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} metering record(s) for service type '{service_type.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_metering_by_service_type: %s", str(e))
        return {"service_type": service_type.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_metering_by_service_type: %s", str(e))
        return {"service_type": service_type.upper(), "error": str(e), "message": str(e)}


def get_metering_by_name(name: str, tool_context: ToolContext) -> dict:
    """
    Get daily metering history records filtered by name.

    Args:
        name: The name to filter metering records by
        tool_context: ADK tool context

    Returns:
        Dictionary with metering records for the given name
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_metering_by_name called for '%s'", name)
    try:
        session = _get_session(tool_context)
        inspector = MeteringDailyHistory(session)
        records = inspector.get_metering_by_name(name)
        return {
            "name": name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} metering record(s) for name '{name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_metering_by_name: %s", str(e))
        return {"name": name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_metering_by_name: %s", str(e))
        return {"name": name.upper(), "error": str(e), "message": str(e)}


def get_total_credits_billed_in_date_range(start_date: str, end_date: str, tool_context: ToolContext) -> dict:
    """
    Get total credits billed across all services within a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        tool_context: ADK tool context

    Returns:
        Dictionary with total credits billed in the date range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_total_credits_billed_in_date_range called for %s to %s", start_date, end_date)
    try:
        session = _get_session(tool_context)
        inspector = MeteringDailyHistory(session)
        records = inspector.get_total_credits_billed_in_date_range(start_date, end_date)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Total credits billed from {start_date} to {end_date}: {len(records)} record(s) returned."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_total_credits_billed_in_date_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_total_credits_billed_in_date_range: %s", str(e))
        return {"start_date": start_date, "end_date": end_date, "error": str(e), "message": str(e)}


def get_all_metering_history(tool_context: ToolContext) -> dict:
    """
    Get the full daily metering history for the account.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with all daily metering history records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_all_metering_history called")
    try:
        session = _get_session(tool_context)
        inspector = MeteringDailyHistory(session)
        records = inspector.get_all_metering_history()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} total daily metering history record(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_all_metering_history: %s", str(e))
        return {"error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_all_metering_history: %s", str(e))
        return {"error": str(e), "message": str(e)}
