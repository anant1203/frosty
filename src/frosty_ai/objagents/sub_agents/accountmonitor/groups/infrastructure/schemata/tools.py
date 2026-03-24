import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.schemata import Schemata


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


def get_schemas_in_database(catalog_name: str, tool_context: ToolContext) -> dict:
    """
    Get all schemas in a specific database from ACCOUNT_USAGE.SCHEMATA.

    Args:
        catalog_name: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with schema records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_schemas_in_database called for '%s'", catalog_name)
    try:
        session = _get_session(tool_context)
        inspector = Schemata(session)
        records = inspector.get_schemas_in_database(catalog_name)
        return {
            "catalog_name": catalog_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} schema(s) in database '{catalog_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_schemas_in_database: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_schemas_in_database: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def is_existing_schema(catalog_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Check whether a schema exists in a given database in ACCOUNT_USAGE.SCHEMATA.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with exists boolean and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("is_existing_schema called for '%s.%s'", catalog_name, schema_name)
    try:
        session = _get_session(tool_context)
        inspector = Schemata(session)
        exists = inspector.is_existing_schema(catalog_name, schema_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "exists": exists,
            "message": f"Schema '{catalog_name.upper()}.{schema_name.upper()}' {'exists' if exists else 'does not exist'} in ACCOUNT_USAGE.SCHEMATA."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in is_existing_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "exists": False, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in is_existing_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "exists": False, "error": str(e), "message": str(e)}


def get_schema(catalog_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Get the definition details for a specific schema from ACCOUNT_USAGE.SCHEMATA.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with schema records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_schema called for '%s.%s'", catalog_name, schema_name)
    try:
        session = _get_session(tool_context)
        inspector = Schemata(session)
        records = inspector.get_schema(catalog_name, schema_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} record(s) for schema '{catalog_name.upper()}.{schema_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_schemas_by_owner(owner_name: str, tool_context: ToolContext) -> dict:
    """
    Get all schemas owned by a specific role from ACCOUNT_USAGE.SCHEMATA.

    Args:
        owner_name: Name of the owning role
        tool_context: ADK tool context

    Returns:
        Dictionary with schema records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_schemas_by_owner called for '%s'", owner_name)
    try:
        session = _get_session(tool_context)
        inspector = Schemata(session)
        records = inspector.get_schemas_by_owner(owner_name)
        return {
            "owner_name": owner_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} schema(s) owned by '{owner_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_schemas_by_owner: %s", str(e))
        return {"owner_name": owner_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_schemas_by_owner: %s", str(e))
        return {"owner_name": owner_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_transient_schemas(catalog_name: str, tool_context: ToolContext) -> dict:
    """
    Get all transient schemas in a specific database from ACCOUNT_USAGE.SCHEMATA.

    Args:
        catalog_name: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with transient schema records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_transient_schemas called for '%s'", catalog_name)
    try:
        session = _get_session(tool_context)
        inspector = Schemata(session)
        records = inspector.get_transient_schemas(catalog_name)
        return {
            "catalog_name": catalog_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} transient schema(s) in database '{catalog_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_transient_schemas: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_transient_schemas: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}


def get_deleted_schemas(catalog_name: str, tool_context: ToolContext) -> dict:
    """
    Get all deleted schemas in a specific database from ACCOUNT_USAGE.SCHEMATA.

    Args:
        catalog_name: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with deleted schema records, count, and message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_deleted_schemas called for '%s'", catalog_name)
    try:
        session = _get_session(tool_context)
        inspector = Schemata(session)
        records = inspector.get_deleted_schemas(catalog_name)
        return {
            "catalog_name": catalog_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} deleted schema(s) in database '{catalog_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_deleted_schemas: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_deleted_schemas: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "records": [], "count": None, "error": str(e), "message": str(e)}
