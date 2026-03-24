import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.pipes import Pipes


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


def get_pipes_in_schema(catalog_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Get all pipe definitions within a specific schema from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with pipe records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_pipes_in_schema called for '%s.%s'", catalog_name, schema_name)
    try:
        session = _get_session(tool_context)
        inspector = Pipes(session)
        records = inspector.get_pipes_in_schema(catalog_name, schema_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} pipe(s) in schema '{catalog_name.upper()}.{schema_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_pipes_in_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_pipes_in_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "error": str(e), "message": str(e)}


def is_existing_pipe(catalog_name: str, schema_name: str, pipe_name: str, tool_context: ToolContext) -> dict:
    """
    Check whether a specific pipe exists in ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        pipe_name: Name of the pipe
        tool_context: ADK tool context

    Returns:
        Dictionary with an exists boolean and a message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("is_existing_pipe called for '%s.%s.%s'", catalog_name, schema_name, pipe_name)
    try:
        session = _get_session(tool_context)
        inspector = Pipes(session)
        exists = inspector.is_existing_pipe(catalog_name, schema_name, pipe_name)
        return {
            "exists": exists,
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "pipe_name": pipe_name.upper(),
            "message": f"Pipe '{catalog_name.upper()}.{schema_name.upper()}.{pipe_name.upper()}' {'exists' if exists else 'does not exist'} in ACCOUNT_USAGE."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in is_existing_pipe: %s", str(e))
        return {"exists": False, "catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "pipe_name": pipe_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in is_existing_pipe: %s", str(e))
        return {"exists": False, "catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "pipe_name": pipe_name.upper(), "error": str(e), "message": str(e)}


def get_pipe(catalog_name: str, schema_name: str, pipe_name: str, tool_context: ToolContext) -> dict:
    """
    Get the definition and details of a specific pipe from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        pipe_name: Name of the pipe
        tool_context: ADK tool context

    Returns:
        Dictionary with pipe records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_pipe called for '%s.%s.%s'", catalog_name, schema_name, pipe_name)
    try:
        session = _get_session(tool_context)
        inspector = Pipes(session)
        records = inspector.get_pipe(catalog_name, schema_name, pipe_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "pipe_name": pipe_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Retrieved {len(records)} record(s) for pipe '{catalog_name.upper()}.{schema_name.upper()}.{pipe_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_pipe: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "pipe_name": pipe_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_pipe: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "pipe_name": pipe_name.upper(), "error": str(e), "message": str(e)}


def get_autoingest_pipes(catalog_name: str, tool_context: ToolContext) -> dict:
    """
    Get all autoingest-enabled pipes within a database from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with autoingest pipe records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_autoingest_pipes called for '%s'", catalog_name)
    try:
        session = _get_session(tool_context)
        inspector = Pipes(session)
        records = inspector.get_autoingest_pipes(catalog_name)
        return {
            "catalog_name": catalog_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} autoingest-enabled pipe(s) in database '{catalog_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_autoingest_pipes: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_autoingest_pipes: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "error": str(e), "message": str(e)}


def get_pipes_by_owner(catalog_name: str, owner_name: str, tool_context: ToolContext) -> dict:
    """
    Get all pipes owned by a specific role within a database from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        owner_name: Name of the owning role
        tool_context: ADK tool context

    Returns:
        Dictionary with pipe records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_pipes_by_owner called for '%s' with owner '%s'", catalog_name, owner_name)
    try:
        session = _get_session(tool_context)
        inspector = Pipes(session)
        records = inspector.get_pipes_by_owner(catalog_name, owner_name)
        return {
            "catalog_name": catalog_name.upper(),
            "owner_name": owner_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} pipe(s) owned by '{owner_name.upper()}' in database '{catalog_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_pipes_by_owner: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "owner_name": owner_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_pipes_by_owner: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "owner_name": owner_name.upper(), "error": str(e), "message": str(e)}


def get_deleted_pipes(catalog_name: str, tool_context: ToolContext) -> dict:
    """
    Get all deleted pipes within a database from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with deleted pipe records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_deleted_pipes called for '%s'", catalog_name)
    try:
        session = _get_session(tool_context)
        inspector = Pipes(session)
        records = inspector.get_deleted_pipes(catalog_name)
        return {
            "catalog_name": catalog_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} deleted pipe(s) in database '{catalog_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_deleted_pipes: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_deleted_pipes: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "error": str(e), "message": str(e)}
