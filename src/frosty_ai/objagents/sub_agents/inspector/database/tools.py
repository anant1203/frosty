from src.infschema.databases import Databases
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


def check_database_exists(database_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a database exists in Snowflake.
    
    Args:
        database_name: Name of the database to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_database_exists called for database '%s'", database_name)
    try:
        session = _get_session(tool_context)
        db_inspector = Databases(session)
        exists = db_inspector.is_existing_database(database_name)
        
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "message": f"Database '{database_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking database '%s': %s", database_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking database '{database_name.upper()}': {str(e)}"
        }


def get_database_properties(database_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed properties of a database.
    
    Args:
        database_name: Name of the database
        tool_context: ADK tool context
        
    Returns:
        Dictionary with database properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_database_properties called for database '%s'", database_name)
    session = _get_session(tool_context)
    db_inspector = Databases(session)

    if not db_inspector.is_existing_database(database_name):
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "message": f"Database '{database_name.upper()}' does not exist"
        }

    try:
        owner = db_inspector.get_database_owner(database_name)
        db_type = db_inspector.get_type_of_db(database_name)
        retention_time = db_inspector.get_retention_time_of_db(database_name)
        created = db_inspector.get_created(database_name)
        
        return {
            "exists": True,
            "database_name": database_name.upper(),
            "owner": owner,
            "type": db_type,
            "retention_time_days": retention_time,
            "created": str(created),
            "message": f"Retrieved properties for database '{database_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for database '%s': %s", database_name, str(e))
        return {
            "exists": True,
            "database_name": database_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error retrieving properties for database '{database_name.upper()}': {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for database '%s': %s", database_name, str(e))
        return {
            "exists": True,
            "database_name": database_name.upper(),
            "error": str(e),
            "message": f"Error retrieving properties for database '{database_name.upper()}': {str(e)}"
        }


def list_all_databases(tool_context: ToolContext) -> dict:
    """
    List all databases accessible to the user.
    
    Args:
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of databases
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_databases called")
    session = _get_session(tool_context)

    try:
        db_inspector = Databases(session)
        db_inspector.use_database('SNOWFLAKE')  # Use SNOWFLAKE database to access the databases view

        # Query all databases
        df = session.table(db_inspector.col._view).select(
            col(db_inspector.col.database_name),
            col(db_inspector.col.is_transient),
            col(db_inspector.col.retention_time),
            col(db_inspector.col.type)
        ).collect()
        
        user_databases = [{
            "name": row[0],
            "is_transient": row[1],
            "retention_time_days": row[2],
            "type": row[3]
        } for row in df]

        return {
            "databases": user_databases,
            "count": len(user_databases),
            "message": f"Found {len(user_databases)} database(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing databases: %s", str(e))
        return {
            "databases": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing databases: {str(e)}"
        }
    except Exception as e:
        logger.error("Error listing databases: %s", str(e))
        return {
            "databases": [],
            "count": 0,
            "error": str(e),
            "message": f"Error listing databases: {str(e)}"
        }


def count_transient_databases(tool_context: ToolContext) -> dict:
    """
    Count transient databases accessible to the user.
    
    Args:
        tool_context: ADK tool context
        
    Returns:
        Dictionary with count of transient databases
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("count_transient_databases called")
    session = _get_session(tool_context)

    try:
        db_inspector = Databases(session)
        db_inspector.use_database('SNOWFLAKE')  # Use SNOWFLAKE database to access the databases view

        df = session.table(db_inspector.col._view).filter(
            col(db_inspector.col.is_transient) == 'YES'
        ).select(col(db_inspector.col.database_name)).collect()

        transient_count = len(df)

        return {
            "transient_count": transient_count,
            "message": f"Found {transient_count} transient database(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error counting transient databases: %s", str(e))
        return {
            "transient_count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error counting transient databases: {str(e)}"
        }
    except Exception as e:
        logger.error("Error counting transient databases: %s", str(e))
        return {
            "transient_count": 0,
            "error": str(e),
            "message": f"Error counting transient databases: {str(e)}"
        }


def filter_databases_by_retention(min_days: int, tool_context: ToolContext) -> dict:
    """
    Filter databases by minimum retention time.
    
    Args:
        min_days: Minimum retention time in days
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered databases
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("filter_databases_by_retention called with min_days=%s", min_days)
    session = _get_session(tool_context)

    try:
        db_inspector = Databases(session)
        db_inspector.use_database('SNOWFLAKE')

        df = session.table(db_inspector.col._view).filter(
            col(db_inspector.col.retention_time) >= min_days
        ).select(
            col(db_inspector.col.database_name),
            col(db_inspector.col.retention_time)
        ).collect()

        filtered_dbs = [{
            "name": row[0],
            "retention_time_days": row[1]
        } for row in df]
        
        return {
            "databases": filtered_dbs,
            "count": len(filtered_dbs),
            "min_retention_days": min_days,
            "message": f"Found {len(filtered_dbs)} database(s) with retention time >= {min_days} days"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering databases by retention: %s", str(e))
        return {
            "databases": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering databases: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering databases by retention: %s", str(e))
        return {
            "databases": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering databases: {str(e)}"
        }
