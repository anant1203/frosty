from src.infschema.stages import Stages
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


def check_stage_exists(database_name: str, schema_name: str, stage_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a stage exists in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        stage_name: Name of the stage to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_stage_exists called for '%s.%s.%s'", database_name, schema_name, stage_name)
    try:
        session = _get_session(tool_context)
        stage_inspector = Stages(session)
        exists = stage_inspector.is_existing_stage(database_name, schema_name, stage_name)
        
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "stage_name": stage_name.upper(),
            "message": f"Stage '{database_name.upper()}.{schema_name.upper()}.{stage_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking stage '%s.%s.%s': %s", database_name, schema_name, stage_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "stage_name": stage_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking stage '{database_name.upper()}.{schema_name.upper()}.{stage_name.upper()}': {str(e)}"
        }


def list_all_stages(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all stages in a schema.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of stages
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_stages called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        stage_inspector = Stages(session)
        stage_inspector.use_database(database_name)

        df = session.table(stage_inspector.col._view).filter(
            (col(stage_inspector.col._stage_catalog) == database_name.upper()) &
            (col(stage_inspector.col._stage_schema) == schema_name.upper())
        ).select(
            col(stage_inspector.col._stage_name),
            col(stage_inspector.col._stage_type)
        ).collect()
        
        stages = [{
            "name": row[0],
            "type": row[1]
        } for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "stages": stages,
            "count": len(stages),
            "message": f"Found {len(stages)} stage(s) in schema '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing stages in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "stages": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing stages: {str(e)}"
        }
    except Exception as e:
        logger.error("Error listing stages in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "stages": [],
            "count": 0,
            "error": str(e),
            "message": f"Error listing stages: {str(e)}"
        }


def get_stage_properties(database_name: str, schema_name: str, stage_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed properties of a stage including type, region, URL, and owner.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        stage_name: Name of the stage
        tool_context: ADK tool context
        
    Returns:
        Dictionary with stage properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_stage_properties called for '%s.%s.%s'", database_name, schema_name, stage_name)
    session = _get_session(tool_context)
    stage_inspector = Stages(session)

    if not stage_inspector.is_existing_stage(database_name, schema_name, stage_name):
        return {
            "exists": False,
            "message": f"Stage '{database_name.upper()}.{schema_name.upper()}.{stage_name.upper()}' does not exist"
        }

    try:
        stage_inspector.use_database(database_name)
        df = session.table(stage_inspector.col._view).filter(
            (col(stage_inspector.col._stage_catalog) == database_name.upper()) &
            (col(stage_inspector.col._stage_schema) == schema_name.upper()) &
            (col(stage_inspector.col._stage_name) == stage_name.upper())
        ).select(
            col(stage_inspector.col._stage_type),
            col(stage_inspector.col._stage_url),
            col(stage_inspector.col._stage_region),
            col(stage_inspector.col._stage_owner),
            col(stage_inspector.col._comment),
            col(stage_inspector.col._created)
        ).collect()
        
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "stage_name": stage_name.upper(),
                "stage_type": row[0],
                "stage_url": row[1],
                "stage_region": row[2],
                "owner": row[3],
                "comment": row[4],
                "created": str(row[5]),
                "message": f"Retrieved properties for stage '{database_name.upper()}.{schema_name.upper()}.{stage_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for stage '%s.%s.%s': %s", database_name, schema_name, stage_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving stage properties: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for stage '%s.%s.%s': %s", database_name, schema_name, stage_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving stage properties: {str(e)}"
        }


def filter_stages_by_type(database_name: str, schema_name: str, stage_type: str, tool_context: ToolContext) -> dict:
    """
    Filter stages by type (INTERNAL or EXTERNAL).
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        stage_type: Stage type to filter by (INTERNAL or EXTERNAL)
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered stages
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("filter_stages_by_type called for '%s.%s' with type '%s'", database_name, schema_name, stage_type)
    session = _get_session(tool_context)
    try:
        stage_inspector = Stages(session)
        stage_inspector.use_database(database_name)

        df = session.table(stage_inspector.col._view).filter(
            (col(stage_inspector.col._stage_catalog) == database_name.upper()) &
            (col(stage_inspector.col._stage_schema) == schema_name.upper()) &
            (col(stage_inspector.col._stage_type) == stage_type.upper())
        ).select(col(stage_inspector.col._stage_name)).collect()
        
        stage_list = [row[0] for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "stage_type": stage_type.upper(),
            "stages": stage_list,
            "count": len(stage_list),
            "message": f"Found {len(stage_list)} {stage_type.upper()} stage(s)"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering stages by type in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "stages": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering stages: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering stages by type in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "stages": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering stages: {str(e)}"
        }
