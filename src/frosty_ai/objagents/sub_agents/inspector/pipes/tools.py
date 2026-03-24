from src.infschema.pipes import Pipes
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


def check_pipe_exists(database_name: str, schema_name: str, pipe_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a pipe exists in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        pipe_name: Name of the pipe to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_pipe_exists called for '%s.%s.%s'", database_name, schema_name, pipe_name)
    try:
        session = _get_session(tool_context)
        pipe_inspector = Pipes(session)
        exists = pipe_inspector.is_existing_pipe(database_name, schema_name, pipe_name)
        
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "pipe_name": pipe_name.upper(),
            "message": f"Pipe '{database_name.upper()}.{schema_name.upper()}.{pipe_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking pipe '%s.%s.%s': %s", database_name, schema_name, pipe_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "pipe_name": pipe_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking pipe '{database_name.upper()}.{schema_name.upper()}.{pipe_name.upper()}': {str(e)}"
        }


def list_all_pipes(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all pipes in a schema.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of pipes
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_pipes called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        pipe_inspector = Pipes(session)
        pipe_inspector.use_database(database_name)

        df = session.table(pipe_inspector.col._view).filter(
            (col(pipe_inspector.col._pipe_catalog) == database_name.upper()) &
            (col(pipe_inspector.col._pipe_schema) == schema_name.upper())
        ).select(col(pipe_inspector.col._pipe_name)).collect()
        
        pipe_list = [row[0] for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "pipes": pipe_list,
            "count": len(pipe_list),
            "message": f"Found {len(pipe_list)} pipe(s) in schema '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing pipes in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "pipes": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing pipes: {str(e)}"
        }
    except Exception as e:
        logger.error("Error listing pipes in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "pipes": [],
            "count": 0,
            "error": str(e),
            "message": f"Error listing pipes: {str(e)}"
        }


def get_pipe_properties(database_name: str, schema_name: str, pipe_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed properties of a pipe including owner, definition, autoingest status, and timestamps.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        pipe_name: Name of the pipe
        tool_context: ADK tool context
        
    Returns:
        Dictionary with pipe properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_pipe_properties called for '%s.%s.%s'", database_name, schema_name, pipe_name)
    session = _get_session(tool_context)
    pipe_inspector = Pipes(session)

    if not pipe_inspector.is_existing_pipe(database_name, schema_name, pipe_name):
        return {
            "exists": False,
            "message": f"Pipe '{database_name.upper()}.{schema_name.upper()}.{pipe_name.upper()}' does not exist"
        }

    try:
        pipe_inspector.use_database(database_name)
        df = session.table(pipe_inspector.col._view).filter(
            (col(pipe_inspector.col._pipe_catalog) == database_name.upper()) &
            (col(pipe_inspector.col._pipe_schema) == schema_name.upper()) &
            (col(pipe_inspector.col._pipe_name) == pipe_name.upper())
        ).select(
            col(pipe_inspector.col._pipe_owner),
            col(pipe_inspector.col._definition),
            col(pipe_inspector.col._is_autoingest_enabled),
            col(pipe_inspector.col._notification_channel_name),
            col(pipe_inspector.col._created),
            col(pipe_inspector.col._last_altered),
            col(pipe_inspector.col._comment),
            col(pipe_inspector.col._pattern)
        ).collect()

        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "pipe_name": pipe_name.upper(),
                "owner": row[0],
                "definition": row[1],
                "is_autoingest_enabled": row[2],
                "notification_channel_name": row[3],
                "created": str(row[4]),
                "last_altered": str(row[5]),
                "comment": row[6],
                "pattern": row[7],
                "message": f"Retrieved properties for pipe '{database_name.upper()}.{schema_name.upper()}.{pipe_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for pipe '%s.%s.%s': %s", database_name, schema_name, pipe_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving pipe properties: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for pipe '%s.%s.%s': %s", database_name, schema_name, pipe_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving pipe properties: {str(e)}"
        }


def filter_pipes_by_autoingest(database_name: str, schema_name: str, autoingest_enabled: str, tool_context: ToolContext) -> dict:
    """
    Filter pipes by their AUTO_INGEST enabled status.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        autoingest_enabled: Filter value for IS_AUTOINGEST_ENABLED (YES or NO)
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered pipes
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("filter_pipes_by_autoingest called for '%s.%s' with autoingest='%s'", database_name, schema_name, autoingest_enabled)
    session = _get_session(tool_context)
    try:
        pipe_inspector = Pipes(session)
        pipe_inspector.use_database(database_name)

        df = session.table(pipe_inspector.col._view).filter(
            (col(pipe_inspector.col._pipe_catalog) == database_name.upper()) &
            (col(pipe_inspector.col._pipe_schema) == schema_name.upper()) &
            (col(pipe_inspector.col._is_autoingest_enabled) == autoingest_enabled.upper())
        ).select(col(pipe_inspector.col._pipe_name)).collect()

        pipe_list = [row[0] for row in df]

        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "autoingest_enabled": autoingest_enabled.upper(),
            "pipes": pipe_list,
            "count": len(pipe_list),
            "message": f"Found {len(pipe_list)} pipe(s) with AUTO_INGEST={autoingest_enabled.upper()}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering pipes by autoingest in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "pipes": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering pipes: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering pipes by autoingest in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "pipes": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering pipes: {str(e)}"
        }
