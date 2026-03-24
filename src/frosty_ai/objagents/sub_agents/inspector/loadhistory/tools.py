from src.infschema.loadhistory import LoadHistory
from src.session import Session
from google.adk.tools import ToolContext
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


def get_load_status_of_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get the load status of a table in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with load status information
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_load_status_of_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        load_history_inspector = LoadHistory(session)
        status = load_history_inspector.get_load_status_of_table(database_name, schema_name, table_name)
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "status": status,
            "message": f"Load status for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {status}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving load status for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "status": "UNKNOWN",
            "error": str(e),
            "message": f"Snowflake SQL error retrieving load status for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving load status for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "status": "UNKNOWN",
            "error": str(e),
            "message": f"Could not retrieve load status for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def get_load_history_of_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get the full load history of a table in Snowflake, including all columns from the LOAD_HISTORY view.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with full load history records
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_load_history_of_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        load_history_inspector = LoadHistory(session)
        rows = load_history_inspector.get_load_history_of_table(database_name, schema_name, table_name)

        records = []
        for row in rows:
            records.append({
                "schema_name": str(row[0]) if row[0] is not None else None,
                "file_name": str(row[1]) if row[1] is not None else None,
                "table_name": str(row[2]) if row[2] is not None else None,
                "last_load_time": str(row[3]) if row[3] is not None else None,
                "status": str(row[4]) if row[4] is not None else None,
                "row_count": int(row[5]) if row[5] is not None else None,
                "row_parsed": int(row[6]) if row[6] is not None else None,
                "first_error_message": str(row[7]) if row[7] is not None else None,
                "first_error_line_number": int(row[8]) if row[8] is not None else None,
                "first_error_character_position": int(row[9]) if row[9] is not None else None,
                "first_error_col_name": str(row[10]) if row[10] is not None else None,
                "error_count": int(row[11]) if row[11] is not None else None,
                "error_limit": int(row[12]) if row[12] is not None else None,
            })

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} load history record(s) for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving load history for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving load history for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving load history for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Could not retrieve load history for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def get_load_errors_of_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get load error details for a table in Snowflake. Returns only records that have errors.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with error records including first error message, line number, column name, and error counts
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_load_errors_of_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        load_history_inspector = LoadHistory(session)
        rows = load_history_inspector.get_load_errors_of_table(database_name, schema_name, table_name)

        records = []
        for row in rows:
            records.append({
                "file_name": str(row[0]) if row[0] is not None else None,
                "last_load_time": str(row[1]) if row[1] is not None else None,
                "status": str(row[2]) if row[2] is not None else None,
                "first_error_message": str(row[3]) if row[3] is not None else None,
                "first_error_line_number": int(row[4]) if row[4] is not None else None,
                "first_error_character_position": int(row[5]) if row[5] is not None else None,
                "first_error_col_name": str(row[6]) if row[6] is not None else None,
                "error_count": int(row[7]) if row[7] is not None else None,
                "error_limit": int(row[8]) if row[8] is not None else None,
            })

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} error record(s) for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving load errors for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving load errors for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving load errors for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Could not retrieve load errors for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def get_most_recent_load_of_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get the most recent load record for a table in Snowflake, sorted by last load time.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with the most recent load record including file name, timestamp, status, row counts, and error info
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_most_recent_load_of_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        load_history_inspector = LoadHistory(session)
        rows = load_history_inspector.get_most_recent_load_of_table(database_name, schema_name, table_name)

        if rows:
            row = rows[0]
            record = {
                "file_name": str(row[0]) if row[0] is not None else None,
                "last_load_time": str(row[1]) if row[1] is not None else None,
                "status": str(row[2]) if row[2] is not None else None,
                "row_count": int(row[3]) if row[3] is not None else None,
                "row_parsed": int(row[4]) if row[4] is not None else None,
                "first_error_message": str(row[5]) if row[5] is not None else None,
                "error_count": int(row[6]) if row[6] is not None else None,
            }
        else:
            record = None

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "record": record,
            "message": f"Most recent load for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {record['status'] if record else 'No records found'}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving most recent load for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "record": None,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving most recent load for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving most recent load for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "record": None,
            "error": str(e),
            "message": f"Could not retrieve most recent load for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def get_row_counts_of_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get row count details from load history for a table in Snowflake.
    Returns rows loaded and rows parsed per file.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with row count records per loaded file
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_row_counts_of_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        load_history_inspector = LoadHistory(session)
        rows = load_history_inspector.get_row_counts_of_table(database_name, schema_name, table_name)

        records = []
        for row in rows:
            records.append({
                "file_name": str(row[0]) if row[0] is not None else None,
                "last_load_time": str(row[1]) if row[1] is not None else None,
                "row_count": int(row[2]) if row[2] is not None else None,
                "row_parsed": int(row[3]) if row[3] is not None else None,
            })

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} row count record(s) for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving row counts for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving row counts for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving row counts for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Could not retrieve row counts for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }


def get_failed_loads_of_table(database_name: str, schema_name: str, table_name: str, tool_context: ToolContext) -> dict:
    """
    Get all failed load records for a table in Snowflake (status = LOAD_FAILED).
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        table_name: Name of the table
        tool_context: ADK tool context
        
    Returns:
        Dictionary with failed load records including error details and row counts
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_failed_loads_of_table called for '%s.%s.%s'", database_name, schema_name, table_name)
    try:
        session = _get_session(tool_context)
        load_history_inspector = LoadHistory(session)
        rows = load_history_inspector.get_failed_loads_of_table(database_name, schema_name, table_name)

        records = []
        for row in rows:
            records.append({
                "file_name": str(row[0]) if row[0] is not None else None,
                "last_load_time": str(row[1]) if row[1] is not None else None,
                "status": str(row[2]) if row[2] is not None else None,
                "first_error_message": str(row[3]) if row[3] is not None else None,
                "first_error_line_number": int(row[4]) if row[4] is not None else None,
                "first_error_character_position": int(row[5]) if row[5] is not None else None,
                "first_error_col_name": str(row[6]) if row[6] is not None else None,
                "error_count": int(row[7]) if row[7] is not None else None,
                "error_limit": int(row[8]) if row[8] is not None else None,
                "row_count": int(row[9]) if row[9] is not None else None,
                "row_parsed": int(row[10]) if row[10] is not None else None,
            })

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} failed load record(s) for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving failed loads for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving failed loads for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving failed loads for '%s.%s.%s': %s", database_name, schema_name, table_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "table_name": table_name.upper(),
            "records": [],
            "count": 0,
            "error": str(e),
            "message": f"Could not retrieve failed loads for table '{database_name.upper()}.{schema_name.upper()}.{table_name.upper()}': {str(e)}"
        }
