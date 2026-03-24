from src.infschema.semanticmetrics import SemanticMetrics
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


def list_semantic_metrics(database_name: str, schema_name: str, semantic_view_name: str, tool_context: ToolContext) -> dict:
    """
    List semantic metric filtered by semantic view.

    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        semantic_view_name: Name of the semantic view
        tool_context: ADK tool context

    Returns:
        Dictionary with list of semantic metric
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_semantic_metrics called for '%s.%s.%s'", database_name, schema_name, semantic_view_name)
    session = _get_session(tool_context)
    try:
        inspector = SemanticMetrics(session)
        inspector.use_database(database_name)
        df = session.table(inspector.col._view).filter(
            (col(inspector.col._semantic_view_catalog) == database_name.upper()) &
            (col(inspector.col._semantic_view_schema) == schema_name.upper()) &
            (col(inspector.col._semantic_view_name) == semantic_view_name.upper())
        ).collect()
        records = [row.as_dict() for row in df]
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "semantic_view_name": semantic_view_name.upper(),
            "records": records,
            "count": len(records),
            "message": f"Found {len(records)} semantic metric record(s) for semantic view '{str(semantic_view_name).upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error in list_semantic_metrics: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Snowflake SQL error: {str(e)}"}
    except Exception as e:
        logger.error("Error in list_semantic_metrics: %s", str(e))
        return {"records": [], "count": None, "error": str(e), "message": f"Error: {str(e)}"}
