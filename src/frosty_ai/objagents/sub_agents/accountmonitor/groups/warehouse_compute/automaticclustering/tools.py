import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.automaticclustering import AutomaticClusteringHistory


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


def get_clustering_history_for_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get automatic clustering history for a specific table.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context

    Returns:
        Dictionary with clustering history records for the table
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_clustering_history_for_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        inspector = AutomaticClusteringHistory(session)
        records = inspector.get_clustering_history_for_table(database_name, schema_name, table_name)
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} clustering history record(s) for '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_clustering_history_for_table: %s", str(e))
        return {"database_name": database_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_clustering_history_for_table: %s", str(e))
        return {"database_name": database_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "error": str(e), "message": str(e)}


def get_clustering_history_in_time_range(start_time: str, end_time: str, tool_context: ToolContext) -> dict:
    """
    Get automatic clustering history records within a time range.

    Args:
        start_time: Start timestamp (e.g. '2024-01-01 00:00:00')
        end_time: End timestamp (e.g. '2024-01-31 23:59:59')
        tool_context: ADK tool context

    Returns:
        Dictionary with clustering history records in the time range
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_clustering_history_in_time_range called for %s to %s", start_time, end_time)
    try:
        session = _get_session(tool_context)
        inspector = AutomaticClusteringHistory(session)
        records = inspector.get_clustering_history_in_time_range(start_time, end_time)
        return {
            "start_time": start_time,
            "end_time": end_time,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} clustering history record(s) between {start_time} and {end_time}."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_clustering_history_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_clustering_history_in_time_range: %s", str(e))
        return {"start_time": start_time, "end_time": end_time, "error": str(e), "message": str(e)}


def get_total_credits_for_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get total automatic clustering credits consumed for a specific table.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context

    Returns:
        Dictionary with total clustering credits for the table
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_total_credits_for_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        inspector = AutomaticClusteringHistory(session)
        records = inspector.get_total_credits_for_table(database_name, schema_name, table_name)
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Total clustering credits for '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {len(records)} record(s) returned."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_total_credits_for_table: %s", str(e))
        return {"database_name": database_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_total_credits_for_table: %s", str(e))
        return {"database_name": database_name.upper(), "schema_name": schema_name.upper(), "table_name": table_name.upper(), "error": str(e), "message": str(e)}


def get_clustering_history_by_database(database_name: str, tool_context: ToolContext) -> dict:
    """
    Get automatic clustering history for all tables in a specific database.

    Args:
        database_name: Name of the database
        tool_context: ADK tool context

    Returns:
        Dictionary with clustering history records for the database
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_clustering_history_by_database called for '%s'", database_name)
    try:
        session = _get_session(tool_context)
        inspector = AutomaticClusteringHistory(session)
        records = inspector.get_clustering_history_by_database(database_name)
        return {
            "database_name": database_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} clustering history record(s) for database '{database_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_clustering_history_by_database: %s", str(e))
        return {"database_name": database_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_clustering_history_by_database: %s", str(e))
        return {"database_name": database_name.upper(), "error": str(e), "message": str(e)}
