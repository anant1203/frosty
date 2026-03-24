from src.infschema.procedures import Procedures
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


def check_procedure_exists(database_name: str, schema_name: str, procedure_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a procedure exists.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        procedure_name: Name of the procedure
        tool_context: ADK tool context

    Returns:
        Dictionary with existence status
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_procedure_exists called for '%s.%s.%s'", database_name, schema_name, procedure_name)
    session = _get_session(tool_context)
    try:
        inspector = Procedures(session)
        exists = inspector.is_existing_procedure(database_name, schema_name, procedure_name)
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "procedure_name": procedure_name.upper(),
            "message": f"Procedure '{database_name.upper()}.{schema_name.upper()}.{procedure_name.upper()}' {'exists' if exists else 'does not exist'}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in check_procedure_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in check_procedure_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}

def list_all_procedures(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all procedure in a schema.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context

    Returns:
        Dictionary with list of procedure
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_procedures called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    try:
        inspector = Procedures(session)
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._procedure_catalog) == database_name.upper()) &
            (col(inspector.col._procedure_schema) == schema_name.upper())
        ).select(col(inspector.col._procedure_name)).collect()
        procedure_list = [row[0] for row in df]
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "procedures": procedure_list,
            "count": len(procedure_list),
            "message": f"Found {len(procedure_list)} procedure(s) in '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_all_procedures: %s", str(e))
        return {"procedures": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_all_procedures: %s", str(e))
        return {"procedures": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}

def get_procedure_properties(database_name: str, schema_name: str, procedure_name: str, tool_context: ToolContext) -> dict:
    """
    Get properties of a procedure.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        procedure_name: Name of the procedure
        tool_context: ADK tool context

    Returns:
        Dictionary with procedure properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_procedure_properties called for '%s.%s.%s'", database_name, schema_name, procedure_name)
    session = _get_session(tool_context)
    try:
        inspector = Procedures(session)
        if not inspector.is_existing_procedure(database_name, schema_name, procedure_name):
            return {
                "exists": False,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "procedure_name": procedure_name.upper(),
                "message": f"Procedure '{database_name.upper()}.{schema_name.upper()}.{procedure_name.upper()}' not found"
            }
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._procedure_catalog) == database_name.upper()) &
            (col(inspector.col._procedure_schema) == schema_name.upper()) &
            (col(inspector.col._procedure_name) == procedure_name.upper())
        ).select(
            col(inspector.col._procedure_owner),
            col(inspector.col._argument_signature),
            col(inspector.col._data_type),
            col(inspector.col._procedure_definition),
            col(inspector.col._procedure_language),
            col(inspector.col._created),
            col(inspector.col._last_altered),
            col(inspector.col._comment)
        ).collect()
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "procedure_name": procedure_name.upper(),
                "owner": row[0],
                "argument_signature": row[1],
                "data_type": row[2],
                "procedure_definition": row[3],
                "procedure_language": row[4],
                "created": str(row[5]),
                "last_altered": str(row[6]),
                "comment": row[7],
                "message": f"Retrieved properties for procedure '{database_name.upper()}.{schema_name.upper()}.{procedure_name.upper()}'"
            }
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "procedure_name": procedure_name.upper(),
            "message": f"Procedure '{database_name.upper()}.{schema_name.upper()}.{procedure_name.upper()}' not found"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in get_procedure_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in get_procedure_properties: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}
