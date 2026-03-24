from src.session import Session
from google.adk.tools import ToolContext
from snowflake.snowpark.exceptions import SnowparkSQLException
import logging


def check_task_exists(database_name: str, schema_name: str, task_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a task exists in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        task_name: Name of the task to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_task_exists called for '%s.%s.%s'", database_name, schema_name, task_name)
    # Get session from tool context using baseobj get_session logic
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

    # Check task existence using SHOW TASKS command
    try:
        query = f"SHOW TASKS LIKE '{task_name.upper()}' IN SCHEMA {database_name}.{schema_name.upper()}"
        result = session.sql(query).collect()
        exists = len(result) > 0
    except SnowparkSQLException:
        exists = False
    except Exception:
        exists = False
    
    return {
        "exists": exists,
        "database_name": database_name.upper(),
        "schema_name": schema_name.upper(),
        "task_name": task_name.upper(),
        "message": f"Task '{database_name.upper()}.{schema_name.upper()}.{task_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
    }
