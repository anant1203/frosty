from src.infschema.tablestoragemetrics import TableStorageMetrics
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


def get_table_storage_metrics(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get storage metrics for a specific table.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context

    Returns:
        Dictionary with table storage metrics
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_table_storage_metrics called for '%s.%s.%s'", database_name, schema_name, table_name)
    session = _get_session(tool_context)
    try:
        inspector = TableStorageMetrics(session)
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._table_catalog) == database_name.upper()) &
            (col(inspector.col._table_schema) == schema_name.upper()) &
            (col(inspector.col._table_name) == table_name.upper())
        ).collect()
        records = [row.as_dict() for row in df]
        if records:
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "table_name": table_name.upper(),
                "properties": records[0],
                "message": f"Retrieved storage metrics for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
            }
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "message": f"Table storage metrics '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}' not found"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_table_storage_metrics: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_table_storage_metrics: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}

def list_tables_storage_metrics(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all table storage metrics in a schema.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with list of table storage metrics
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_tables_storage_metrics called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        inspector = TableStorageMetrics(session)
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._table_catalog) == database_name.upper()) &
            (col(inspector.col._table_schema) == schema_name.upper())
        ).collect()
        records = [row.as_dict() for row in df]
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} table storage metrics record(s) in '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_tables_storage_metrics: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_tables_storage_metrics: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}
