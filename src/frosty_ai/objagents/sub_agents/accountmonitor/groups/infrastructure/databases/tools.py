import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.databases import Databases


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


def get_all_active_databases(tool_context: ToolContext) -> dict:
    """
    Get all active databases in the account from ACCOUNT_USAGE.DATABASES.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with active database records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_all_active_databases called")
    try:
        session = _get_session(tool_context)
        inspector = Databases(session)
        records = inspector.get_all_active_databases()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} active database(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_all_active_databases: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_all_active_databases: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def is_existing_database(database_name: str, tool_context: ToolContext) -> dict:
    """
    Check whether a database exists in ACCOUNT_USAGE.DATABASES.

    Args:
        database_name: Name of the database to check
        tool_context: ADK tool context

    Returns:
        Dictionary with exists boolean and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("is_existing_database called for '%s'", database_name)
    try:
        session = _get_session(tool_context)
        inspector = Databases(session)
        exists = inspector.is_existing_database(database_name)
        return {
            "database_name": database_name.upper(),
            "exists": exists,
            "message": f"Database '{database_name.upper()}' {'exists' if exists else 'does not exist'} in ACCOUNT_USAGE.DATABASES."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in is_existing_database: %s", str(e))
        return {"database_name": database_name.upper(), "exists": False, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in is_existing_database: %s", str(e))
        return {"database_name": database_name.upper(), "exists": False, "error": str(e), "message": str(e)}


def get_database(database_name: str, tool_context: ToolContext) -> dict:
    """
    Get the definition details for a specific database from ACCOUNT_USAGE.DATABASES.

    Args:
        database_name: Name of the database
        tool_context: ADK tool context

    Returns:
        Dictionary with database records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_database called for '%s'", database_name)
    try:
        session = _get_session(tool_context)
        inspector = Databases(session)
        records = inspector.get_database(database_name)
        return {
            "database_name": database_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} record(s) for database '{database_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_database: %s", str(e))
        return {"database_name": database_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_database: %s", str(e))
        return {"database_name": database_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_databases_by_owner(owner_name: str, tool_context: ToolContext) -> dict:
    """
    Get all databases owned by a specific role from ACCOUNT_USAGE.DATABASES.

    Args:
        owner_name: Name of the owning role
        tool_context: ADK tool context

    Returns:
        Dictionary with database records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_databases_by_owner called for '%s'", owner_name)
    try:
        session = _get_session(tool_context)
        inspector = Databases(session)
        records = inspector.get_databases_by_owner(owner_name)
        return {
            "owner_name": owner_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} database(s) owned by '{owner_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_databases_by_owner: %s", str(e))
        return {"owner_name": owner_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_databases_by_owner: %s", str(e))
        return {"owner_name": owner_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_transient_databases(tool_context: ToolContext) -> dict:
    """
    Get all transient databases from ACCOUNT_USAGE.DATABASES.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with transient database records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_transient_databases called")
    try:
        session = _get_session(tool_context)
        inspector = Databases(session)
        records = inspector.get_transient_databases()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} transient database(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_transient_databases: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_transient_databases: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}


def get_deleted_databases(tool_context: ToolContext) -> dict:
    """
    Get all deleted databases from ACCOUNT_USAGE.DATABASES.

    Args:
        tool_context: ADK tool context

    Returns:
        Dictionary with deleted database records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_deleted_databases called")
    try:
        session = _get_session(tool_context)
        inspector = Databases(session)
        records = inspector.get_deleted_databases()
        return {
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} deleted database(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_deleted_databases: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_deleted_databases: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": str(e)}
