from src.infschema.cortexsearchscoringprofiles import CortexSearchScoringProfiles
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


def list_scoring_profiles(database_name: str, schema_name: str, service_name: str, tool_context: ToolContext) -> dict:
    """
    List scoring profile filtered by cortex search service.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        service_name: Name of the cortex search service
        tool_context: ADK tool context

    Returns:
        Dictionary with list of scoring profile
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_scoring_profiles called for '%s.%s.%s'", database_name, schema_name, service_name)
    session = _get_session(tool_context)
    try:
        inspector = CortexSearchScoringProfiles(session)
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._service_catalog) == database_name.upper()) &
            (col(inspector.col._service_schema) == schema_name.upper()) &
            (col(inspector.col._service_name) == service_name.upper())
        ).select(col(inspector.col._profile_name)).collect()
        profile_list = [row[0] for row in df]
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "service_name": service_name.upper(),
            "scoring_profiles": profile_list,
            "count": len(profile_list),
            "message": f"Found {len(profile_list)} scoring profile(s) for cortex search service '{str(service_name).upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_scoring_profiles: %s", str(e))
        return {"scoring_profiles": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_scoring_profiles: %s", str(e))
        return {"scoring_profiles": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}

def check_scoring_profile_exists(database_name: str, schema_name: str, service_name: str, profile_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a scoring profile exists for a cortex search service.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        service_name: Name of the cortex search service
        profile_name: Name of the scoring profile
        tool_context: ADK tool context

    Returns:
        Dictionary with existence status
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_scoring_profile_exists called for '%s.%s.%s.%s'", database_name, schema_name, service_name, profile_name)
    session = _get_session(tool_context)
    try:
        inspector = CortexSearchScoringProfiles(session)
        exists = inspector.is_existing_scoring_profile(database_name, schema_name, service_name, profile_name)
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "service_name": service_name.upper(),
            "profile_name": profile_name.upper(),
            "message": f"Scoring profile '{profile_name.upper()}' for service '{service_name.upper()}' {'exists' if exists else 'does not exist'}"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in check_scoring_profile_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in check_scoring_profile_exists: %s", str(e))
        return {"exists": False, "error": str(e), "message": f"Error: {str(e)}"}
