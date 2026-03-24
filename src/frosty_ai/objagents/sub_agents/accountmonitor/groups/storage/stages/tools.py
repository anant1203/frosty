import logging
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
from src.session import Session
from src.accountusage.stages import Stages


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


def get_stages_in_schema(catalog_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Get all stage definitions within a specific schema from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with stage records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_stages_in_schema called for '%s.%s'", catalog_name, schema_name)
    try:
        session = _get_session(tool_context)
        inspector = Stages(session)
        records = inspector.get_stages_in_schema(catalog_name, schema_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} stage(s) in schema '{catalog_name.upper()}.{schema_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_stages_in_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_stages_in_schema: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "error": str(e), "message": str(e)}


def get_stages_in_database(catalog_name: str, tool_context: ToolContext) -> dict:
    """
    Get all stage definitions within a database from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        tool_context: ADK tool context

    Returns:
        Dictionary with stage records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_stages_in_database called for '%s'", catalog_name)
    try:
        session = _get_session(tool_context)
        inspector = Stages(session)
        records = inspector.get_stages_in_database(catalog_name)
        return {
            "catalog_name": catalog_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} stage(s) in database '{catalog_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_stages_in_database: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_stages_in_database: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "error": str(e), "message": str(e)}


def is_existing_stage(catalog_name: str, schema_name: str, stage_name: str, tool_context: ToolContext) -> dict:
    """
    Check whether a specific stage exists in ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        stage_name: Name of the stage
        tool_context: ADK tool context

    Returns:
        Dictionary with an exists boolean and a message
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("is_existing_stage called for '%s.%s.%s'", catalog_name, schema_name, stage_name)
    try:
        session = _get_session(tool_context)
        inspector = Stages(session)
        exists = inspector.is_existing_stage(catalog_name, schema_name, stage_name)
        return {
            "exists": exists,
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "stage_name": stage_name.upper(),
            "message": f"Stage '{catalog_name.upper()}.{schema_name.upper()}.{stage_name.upper()}' {'exists' if exists else 'does not exist'} in ACCOUNT_USAGE."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in is_existing_stage: %s", str(e))
        return {"exists": False, "catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "stage_name": stage_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in is_existing_stage: %s", str(e))
        return {"exists": False, "catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "stage_name": stage_name.upper(), "error": str(e), "message": str(e)}


def get_stages_by_type(stage_type: str, tool_context: ToolContext) -> dict:
    """
    Get all stage definitions filtered by stage type from ACCOUNT_USAGE.

    Args:
        stage_type: The stage type to filter by (e.g. 'Internal Named', 'External Named')
        tool_context: ADK tool context

    Returns:
        Dictionary with stage records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_stages_by_type called for type '%s'", stage_type)
    try:
        session = _get_session(tool_context)
        inspector = Stages(session)
        records = inspector.get_stages_by_type(stage_type)
        return {
            "stage_type": stage_type,
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Found {len(records)} stage(s) of type '{stage_type}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_stages_by_type: %s", str(e))
        return {"stage_type": stage_type, "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_stages_by_type: %s", str(e))
        return {"stage_type": stage_type, "error": str(e), "message": str(e)}


def get_stage(catalog_name: str, schema_name: str, stage_name: str, tool_context: ToolContext) -> dict:
    """
    Get the definition and details of a specific stage from ACCOUNT_USAGE.

    Args:
        catalog_name: Name of the database (catalog)
        schema_name: Name of the schema
        stage_name: Name of the stage
        tool_context: ADK tool context

    Returns:
        Dictionary with stage records and count
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_stage called for '%s.%s.%s'", catalog_name, schema_name, stage_name)
    try:
        session = _get_session(tool_context)
        inspector = Stages(session)
        records = inspector.get_stage(catalog_name, schema_name, stage_name)
        return {
            "catalog_name": catalog_name.upper(),
            "schema_name": schema_name.upper(),
            "stage_name": stage_name.upper(),
            "records": [str(r) for r in records],
            "count": len(records),
            "message": f"Retrieved {len(records)} record(s) for stage '{catalog_name.upper()}.{schema_name.upper()}.{stage_name.upper()}'."
        }
    except SnowparkSQLException as e:
        logger.error("SQL error in get_stage: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "stage_name": stage_name.upper(), "error": str(e), "message": str(e)}
    except Exception as e:
        logger.error("Error in get_stage: %s", str(e))
        return {"catalog_name": catalog_name.upper(), "schema_name": schema_name.upper(), "stage_name": stage_name.upper(), "error": str(e), "message": str(e)}
