from src.infschema.cortexsearchservices import CortexSearchServices
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


def check_cortex_search_exists(database_name: str, schema_name: str, service_name: str, tool_context: ToolContext) -> dict:
    """
    Check if a cortex search service exists in Snowflake.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        service_name: Name of the cortex search service to check
        tool_context: ADK tool context
        
    Returns:
        Dictionary with existence status and details
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("check_cortex_search_exists called for '%s.%s.%s'", database_name, schema_name, service_name)
    try:
        session = _get_session(tool_context)
        inspector = CortexSearchServices(session)
        exists = inspector.is_existing_cortex_search(database_name, schema_name, service_name)
        
        return {
            "exists": exists,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "service_name": service_name.upper(),
            "message": f"Cortex search service '{database_name.upper()}.{schema_name.upper()}.{service_name.upper()}' {'exists' if exists else 'does not exist'} in Snowflake account"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error checking cortex search service '%s.%s.%s': %s", database_name, schema_name, service_name, str(e))
        return {
            "exists": False,
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "service_name": service_name.upper(),
            "error": str(e),
            "message": f"Snowflake SQL error checking cortex search service '{database_name.upper()}.{schema_name.upper()}.{service_name.upper()}': {str(e)}"
        }


def list_cortex_search_in_schema(database_name: str, schema_name: str, tool_context: ToolContext) -> dict:
    """
    List all cortex search services in a schema.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        tool_context: ADK tool context
        
    Returns:
        Dictionary with list of cortex search services
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("list_cortex_search_in_schema called for '%s.%s'", database_name, schema_name)
    try:
        session = _get_session(tool_context)
        inspector = CortexSearchServices(session)
        services = inspector.get_all_cortex_search_in_schema(database_name, schema_name)
        
        service_list = [row[0] for row in services]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "services": service_list,
            "count": len(service_list),
            "message": f"Found {len(service_list)} cortex search service(s) in schema '{database_name.upper()}.{schema_name.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error listing cortex search services in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "services": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error listing cortex search services: {str(e)}"
        }
    except Exception as e:
        logger.error("Error listing cortex search services in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "services": [],
            "count": 0,
            "error": str(e),
            "message": f"Error listing cortex search services: {str(e)}"
        }


def get_cortex_search_properties(database_name: str, schema_name: str, service_name: str, tool_context: ToolContext) -> dict:
    """
    Get detailed properties of a cortex search service including definition, search column,
    attributes, warehouse, target lag, indexing state, serving state, and more.
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        service_name: Name of the cortex search service
        tool_context: ADK tool context
        
    Returns:
        Dictionary with cortex search service properties
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("get_cortex_search_properties called for '%s.%s.%s'", database_name, schema_name, service_name)
    session = _get_session(tool_context)
    inspector = CortexSearchServices(session)

    if not inspector.is_existing_cortex_search(database_name, schema_name, service_name):
        return {
            "exists": False,
            "message": f"Cortex search service '{database_name.upper()}.{schema_name.upper()}.{service_name.upper()}' does not exist"
        }

    try:
        props = inspector.get_cortex_search_properties(database_name, schema_name, service_name)
        
        if props:
            return {
                "exists": True,
                "database_name": database_name.upper(),
                "schema_name": schema_name.upper(),
                "service_name": service_name.upper(),
                "created": str(props["created"]),
                "definition": props["definition"],
                "search_column": props["search_column"],
                "attribute_columns": props["attribute_columns"],
                "columns": props["columns"],
                "target_lag": props["target_lag"],
                "warehouse": props["warehouse"],
                "comment": props["comment"],
                "service_query_url": props["service_query_url"],
                "owner": props["owner"],
                "owner_role_type": props["owner_role_type"],
                "data_fresh_as_of": str(props["data_fresh_as_of"]),
                "data_timestamp": str(props["data_timestamp"]),
                "source_data_bytes": props["source_data_bytes"],
                "source_data_num_rows": props["source_data_num_rows"],
                "indexing_state": props["indexing_state"],
                "indexing_error": props["indexing_error"],
                "serving_state": props["serving_state"],
                "serving_data_bytes": props["serving_data_bytes"],
                "embedding_model": props["embedding_model"],
                "message": f"Retrieved properties for cortex search service '{database_name.upper()}.{schema_name.upper()}.{service_name.upper()}'"
            }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error retrieving properties for cortex search service '%s.%s.%s': %s", database_name, schema_name, service_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Snowflake SQL error retrieving cortex search service properties: {str(e)}"
        }
    except Exception as e:
        logger.error("Error retrieving properties for cortex search service '%s.%s.%s': %s", database_name, schema_name, service_name, str(e))
        return {
            "exists": True,
            "error": str(e),
            "message": f"Error retrieving cortex search service properties: {str(e)}"
        }


def filter_cortex_search_by_indexing_state(database_name: str, schema_name: str, indexing_state: str, tool_context: ToolContext) -> dict:
    """
    Filter cortex search services by indexing state (RUNNING or SUSPENDED).
    
    Args:
        database_name: Name of the database
        schema_name: Name of the schema
        indexing_state: Indexing state to filter by (RUNNING or SUSPENDED)
        tool_context: ADK tool context
        
    Returns:
        Dictionary with filtered cortex search services
    """
    logger = logging.getLogger(tool_context.state.get("app:LOGGER")).getChild(__name__)
    logger.debug("filter_cortex_search_by_indexing_state called for '%s.%s' with state '%s'", database_name, schema_name, indexing_state)
    session = _get_session(tool_context)
    try:
        inspector = CortexSearchServices(session)
        inspector.use_database(database_name)

        df = session.table(inspector.col._view).filter(
            (col(inspector.col._service_catalog) == database_name.upper()) &
            (col(inspector.col._service_schema) == schema_name.upper()) &
            (col(inspector.col._indexing_state) == indexing_state.upper())
        ).select(col(inspector.col._service_name)).collect()
        
        service_list = [row[0] for row in df]
        
        return {
            "database_name": database_name.upper(),
            "schema_name": schema_name.upper(),
            "indexing_state": indexing_state.upper(),
            "services": service_list,
            "count": len(service_list),
            "message": f"Found {len(service_list)} cortex search service(s) with indexing state '{indexing_state.upper()}'"
        }
    except SnowparkSQLException as e:
        logger.error("Snowflake SQL error filtering cortex search services by indexing state in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "services": [],
            "count": 0,
            "error": str(e),
            "message": f"Snowflake SQL error filtering cortex search services: {str(e)}"
        }
    except Exception as e:
        logger.error("Error filtering cortex search services by indexing state in '%s.%s': %s", database_name, schema_name, str(e))
        return {
            "services": [],
            "count": 0,
            "error": str(e),
            "message": f"Error filtering cortex search services: {str(e)}"
        }
