import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.tablestoragemetrics import TableStorageMetrics


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


def get_storage_metrics_for_table(table_catalog: str, table_schema: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get storage metrics (active bytes, failsafe bytes, time-travel bytes) for a specific table.

    Args:
        table_catalog: Name of the database (catalog)
        table_schema: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context

    Returns:
        Dictionary with storage metrics records for the table
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_storage_metrics_for_table called for '%s.%s.%s'", table_catalog, table_schema, table_name)
    try:
        session = _get_session(tool_context)
        inspector = TableStorageMetrics(session)
        records = inspector.get_storage_metrics_for_table(table_catalog, table_schema, table_name)
        return {
            "table_catalog": table_catalog.upper(),
            "table_schema": table_schema.upper(),
            "table_name": table_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Storage metrics for '{table_catalog.upper()}.{table_schema.upper()}.{table_name.upper()}': {len(records)} record(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_storage_metrics_for_table: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "table_schema": table_schema.upper(), "table_name": table_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_storage_metrics_for_table: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "table_schema": table_schema.upper(), "table_name": table_name.upper(), "error": str(e), "message": str(e)}


def get_storage_metrics_for_schema(table_catalog: str, table_schema: str, tool_context: ToolContext) -> dict:
    """
    Get storage metrics for all tables within a schema.

    Args:
        table_catalog: Name of the database (catalog)
        table_schema: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with storage metrics records for all tables in the schema
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_storage_metrics_for_schema called for '%s.%s'", table_catalog, table_schema)
    try:
        session = _get_session(tool_context)
        inspector = TableStorageMetrics(session)
        records = inspector.get_storage_metrics_for_schema(table_catalog, table_schema)
        return {
            "table_catalog": table_catalog.upper(),
            "table_schema": table_schema.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Storage metrics for schema '{table_catalog.upper()}.{table_schema.upper()}': {len(records)} table(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_storage_metrics_for_schema: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "table_schema": table_schema.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_storage_metrics_for_schema: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "table_schema": table_schema.upper(), "error": str(e), "message": str(e)}


def get_storage_metrics_for_database(table_catalog: str, tool_context: ToolContext) -> dict:
    """
    Get storage metrics for all tables within a database.

    Args:
        table_catalog: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with storage metrics records for all tables in the database
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_storage_metrics_for_database called for '%s'", table_catalog)
    try:
        session = _get_session(tool_context)
        inspector = TableStorageMetrics(session)
        records = inspector.get_storage_metrics_for_database(table_catalog)
        return {
            "table_catalog": table_catalog.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Storage metrics for database '{table_catalog.upper()}': {len(records)} table(s)."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_storage_metrics_for_database: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_storage_metrics_for_database: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "error": str(e), "message": str(e)}


def get_deleted_tables(table_catalog: str, tool_context: ToolContext) -> dict:
    """
    Get storage metrics for tables that have been deleted within a database.

    Args:
        table_catalog: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with records for deleted tables in the database
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_deleted_tables called for '%s'", table_catalog)
    try:
        session = _get_session(tool_context)
        inspector = TableStorageMetrics(session)
        records = inspector.get_deleted_tables(table_catalog)
        return {
            "table_catalog": table_catalog.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} deleted table(s) in database '{table_catalog.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_deleted_tables: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_deleted_tables: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "error": str(e), "message": str(e)}


def get_tables_with_failsafe_bytes(table_catalog: str, min_failsafe_bytes: int, tool_context: ToolContext) -> dict:
    """
    Get tables consuming failsafe storage above a minimum byte threshold.

    Args:
        table_catalog: Name of the database (catalog)
        min_failsafe_bytes: Minimum failsafe bytes threshold
        tool_context: ADK tool context

    Returns:
        Dictionary with records for tables exceeding the failsafe bytes threshold
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_tables_with_failsafe_bytes called for '%s' with min_failsafe_bytes=%d", table_catalog, min_failsafe_bytes)
    try:
        session = _get_session(tool_context)
        inspector = TableStorageMetrics(session)
        records = inspector.get_tables_with_failsafe_bytes(table_catalog, min_failsafe_bytes)
        return {
            "table_catalog": table_catalog.upper(),
            "min_failsafe_bytes": min_failsafe_bytes,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} table(s) in '{table_catalog.upper()}' with failsafe bytes >= {min_failsafe_bytes}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_tables_with_failsafe_bytes: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "min_failsafe_bytes": min_failsafe_bytes, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_tables_with_failsafe_bytes: %s", str(e))
        return {"table_catalog": table_catalog.upper(), "min_failsafe_bytes": min_failsafe_bytes, "error": str(e), "message": str(e)}
