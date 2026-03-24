from src.infschema.schemata import Schemata
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


def check_schema_exists(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a schema exists in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_schema_exists called for '%s.%s'", database_name, schema_name)
    try:
        session = _get_session(tool_context)
        schema_inspector = Schemata(session)
        exists = schema_inspector.is_existing_schema(database_name, schema_name)
        
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "message": f"Schema '{database_name.upper()}.{schema_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking schema '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking schema '{database_name.upper()}.{schema_name.upper()}': {str(e)}"
        }


def list_all_schemas(database_name: str, tool_context: ToolContext) -> dict:
    """
    List all schemas in a database.
    
    Args:
        database_name: Name of the database
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of schemas
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_all_schemas called for '%s'", database_name)
    session = _get_session(tool_context)
    try:
        schema_inspector = Schemata(session)
        schema_inspector.use_database(database_name)

        df = session.table(schema_inspector.col._view).filter(
            col(schema_inspector.col.catalog_name) == database_name.upper()
        ).select(
            col(schema_inspector.col.schema_name),
            col(schema_inspector.col.is_transient),
            col(schema_inspector.col.is_managed_access)
        ).collect()
        
        SYSTEM_SCHEMAS = {"PUBLIC", "INFORMATION_SCHEMA"}
        schemas = [{
            "name": row[0],
            "is_transient": row[1],
            "is_managed_access": row[2]
        } for row in df if row[0].upper() not in SYSTEM_SCHEMAS]

        return {
            "database_name": database_name.upper(),
            "schemas": schemas,
            "count": len(schemas),
            "message": f"Found {len(schemas)} schema(s) in database '{database_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing schemas in '%s': %s", database_name, str(e))
        return {
            "schemas": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing schemas: {str(e)}"
        }
    except Exception as e:
        logger.error("Error listing schemas in '%s': %s", database_name, str(e))
        return {
            "schemas": [],
            "count": 0,
            "error": str(e),
            "message": f"Error listing schemas: {str(e)}"
        }


def get_schema_properties(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed properties of a schema.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context
        
    Returns:
        Dictionary with schema properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_schema_properties called for '%s.%s'", database_name, schema_name)
    session = _get_session(tool_context)
    schema_inspector = Schemata(session)

    if not schema_inspector.is_existing_schema(database_name, schema_name):
        return {
            "exists": False,
            "message": f"Schema '{database_name.upper()}.{schema_name.upper()}' does not exist"
        }

    try:
        schema_inspector.use_database(database_name)
        df = session.table(schema_inspector.col._view).filter(
            (col(schema_inspector.col.catalog_name) == database_name.upper()) &
            (col(schema_inspector.col.schema_name) == schema_name.upper())
        ).select(
            col(schema_inspector.col.schema_owner),
            col(schema_inspector.col.is_transient),
            col(schema_inspector.col.is_managed_access),
            col(schema_inspector.col.retention_time),
            col(schema_inspector.col.created),
            col(schema_inspector.col.comment)
        ).collect()
        
        if df:
            row = df[0]
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "owner": row[0],
                "is_transient": row[1],
                "is_managed_access": row[2],
                "retention_time_days": row[3],
                "created": str(row[4]),
                "comment": row[5],
                "message": f"Retrieved properties for schema '{database_name.upper()}.{schema_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for schema '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving schema properties: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for schema '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving schema properties: {str(e)}"
        }


def count_transient_schemas(database_name: str, tool_context: ToolContext) -> dict:
    """
    Count transient schemas in a database.
    
    Args:
        database_name: Name of the database
        tool_context: ADK tool context
        
    Returns:
        Dictionary with count of transient schemas
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("count_transient_schemas called for '%s'", database_name)
    session = _get_session(tool_context)
    try:
        schema_inspector = Schemata(session)
        schema_inspector.use_database(database_name)

        SYSTEM_SCHEMAS = {"PUBLIC", "INFORMATION_SCHEMA"}
        df = session.table(schema_inspector.col._view).filter(
            (col(schema_inspector.col.catalog_name) == database_name.upper()) &
            (col(schema_inspector.col.is_transient) == 'YES') &
            (~col(schema_inspector.col.schema_name).isin(list(SYSTEM_SCHEMAS)))
        ).count()
        
        return {
            "database_name": database_name.upper(),
            "transient_count": df,
            "message": f"Found {df} transient schema(s) in database '{database_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error counting transient schemas in '%s': %s", database_name, str(e))
        return {
            "transient_count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error counting transient schemas: {str(e)}"
        }
    except Exception as e:
        logger.error("Error counting transient schemas in '%s': %s", database_name, str(e))
        return {
            "transient_count": 0,
            "error": str(e),
            "message": f"Error counting transient schemas: {str(e)}"
        }


def filter_schemas_by_retention(database_name: str, min_days: int, tool_context: ToolContext) -> dict:
    """
    Filter schemas by minimum retention time.
    
    Args:
        database_name: Name of the database
        min_days: Minimum retention time in days
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered schemas
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("filter_schemas_by_retention called for '%s' with min_days=%s", database_name, min_days)
    session = _get_session(tool_context)
    try:
        schema_inspector = Schemata(session)
        schema_inspector.use_database(database_name)

        df = session.table(schema_inspector.col._view).filter(
            (col(schema_inspector.col.catalog_name) == database_name.upper()) &
            (col(schema_inspector.col.retention_time) >= min_days)
        ).select(
            col(schema_inspector.col.schema_name),
            col(schema_inspector.col.retention_time)
        ).collect()
        
        SYSTEM_SCHEMAS = {"PUBLIC", "INFORMATION_SCHEMA"}
        schemas = [{
            "name": row[0],
            "retention_time_days": row[1]
        } for row in df if row[0].upper() not in SYSTEM_SCHEMAS]
        
        return {
            "database_name": database_name.upper(),
            "schemas": schemas,
            "count": len(schemas),
            "min_retention_days": min_days,
            "message": f"Found {len(schemas)} schema(s) with retention time >= {min_days} days"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering schemas by retention in '%s': %s", database_name, str(e))
        return {
            "schemas": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering schemas: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering schemas by retention in '%s': %s", database_name, str(e))
        return {
            "schemas": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering schemas: {str(e)}"
        }
