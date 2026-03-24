import logging
import time

from google.adk.tools import ToolContext
from src.frosty_ai.telemetry import tracer, query_counter, query_errors, query_latency


def execute_query(query: str, tool_context: ToolContext) -> dict:
    """
    Execute a Snowflake SQL query using the session credentials stored in the
    current ADK ToolContext state.

    This is the single execution tool available to every specialist agent.
    The agent is responsible for generating the correct Snowflake SQL statement;
    this tool merely opens a Snowpark session, runs the query, and returns
    the result.

    Args:
        query: The complete Snowflake SQL statement to execute.
        tool_context: ADK tool context that carries session credentials and
            state (tasks performed, queries executed, etc.).

    Returns:
        A dictionary with ``success`` (bool), the executed ``query``, any
        ``result`` rows, and updated task/query tracking information.
    """
    with tracer.start_as_current_span("snowflake.execute_query") as span:
        span.set_attribute("db.system", "snowflake")
        span.set_attribute("db.statement", query[:500])
        t0 = time.monotonic()
        try:
            logger_name = tool_context.state.get("app:LOGGER")
            logger = logging.getLogger(logger_name).getChild(__name__) if logger_name is not None else logging.getLogger(__name__)
            logger.info("execute_query called with: %s", query[:500])

            # --- Obtain a Snowflake session from ToolContext state ---------------
            from src.session import Session as SnowflakeSession
            username = tool_context.state.get("user:SNOWFLAKE_USER_NAME")
            account = tool_context.state.get("app:ACCOUNT_IDENTIFIER")

            span.set_attribute("db.user", username or "")
            span.set_attribute("db.snowflake.account", account or "")

            if not username or not account:
                missing = [k for k, v in {"username": username, "account": account}.items() if not v]
                raise ValueError(f"Missing Snowflake credentials in session state: {', '.join(missing)}")

            session_inst = SnowflakeSession()
            session_inst.set_user(username)
            session_inst.set_account(account)
            session_inst.set_password(tool_context.state.get("user:USER_PASSWORD"))
            if tool_context.state.get("user:AUTHENTICATOR"):
                session_inst.set_authenticator(tool_context.state.get("user:AUTHENTICATOR"))
            if tool_context.state.get("user:ROLE"):
                session_inst.set_role(tool_context.state.get("user:ROLE"))
            if tool_context.state.get("app:WAREHOUSE"):
                session_inst.set_warehouse(tool_context.state.get("app:WAREHOUSE"))
            if tool_context.state.get("app:DATABASE"):
                session_inst.set_database(tool_context.state.get("app:DATABASE"))
            session = session_inst.get_session()

            # --- Safety gate: block DROP unconditionally -------------------------
            if "DROP " in query.upper():
                logger.warning("Safety gate blocked DROP query: %s", query[:500])
                return {
                    "success": False,
                    "query": query,
                    "message": "Query blocked: 'DROP' is not permitted. Use ALTER or CREATE IF NOT EXISTS instead.",
                }

            # --- Safety gate: require human approval for CREATE OR REPLACE ------
            if "CREATE OR REPLACE" in query.upper():
                logger.warning("Safety gate triggered for CREATE OR REPLACE: %s", query[:500])
                from ._spinner import spinner as _sp
                from rich.console import Console as _Console
                from rich.panel import Panel as _Panel
                _con = _Console()
                _sp.stop()
                from rich.syntax import Syntax as _Syntax
                _con.print(_Panel(
                    _Syntax(query, "sql", theme="monokai", word_wrap=True),
                    title="[bold red]⚠  CREATE OR REPLACE — Approval Required[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                ))
                try:
                    import sys as _sys
                    _sys.stdout.write("  Proceed? [yes/no]: ")
                    _sys.stdout.flush()
                    answer = _sys.stdin.readline().strip().lower()
                except (EOFError, KeyboardInterrupt):
                    answer = "no"
                if answer not in ("yes", "y"):
                    logger.info("User declined CREATE OR REPLACE query: %s", query[:500])
                    return {
                        "success": False,
                        "query": query,
                        "message": "Query blocked: user declined execution of 'CREATE OR REPLACE' statement.",
                    }
                logger.info("User approved CREATE OR REPLACE query: %s", query[:500])

            # --- Execute the query -----------------------------------------------
            logger.info("Executing query: %.500s", query)
            result_rows = session.sql(query).collect()
            logger.debug("Query executed successfully, rows returned: %d", len(result_rows))

            # Convert Row objects to plain dicts for serialisation
            result_dicts = [row.as_dict() if hasattr(row, "as_dict") else str(row) for row in result_rows]

            # --- Update session state tracking -----------------------------------
            tasks = tool_context.state.get("app:TASKS_PERFORMED") or []
            task_entry = {
                "OPERATION_STATUS": "SUCCESS",
                "GENERATED_QUERY": query,
            }
            tasks.append(task_entry)
            tool_context.state["app:TASKS_PERFORMED"] = tasks

            queries = tool_context.state.get("user:QUERIES_EXECUTED") or []
            queries.append(query)
            tool_context.state["user:QUERIES_EXECUTED"] = queries

            query_counter.add(1, {"status": "success"})
            query_latency.record((time.monotonic() - t0) * 1000, {"status": "success"})
            span.set_attribute("db.rows_returned", len(result_dicts))
            return {
                "success": True,
                "query": query,
                "result": result_dicts,
                "message": f"Query executed successfully. Rows returned: {len(result_dicts)}",
            }

        except Exception as e:
            logger = logging.getLogger(__name__)
            query_errors.add(1, {"error_type": type(e).__name__})
            query_latency.record((time.monotonic() - t0) * 1000, {"status": "error"})
            from opentelemetry import trace as _t
            span.set_status(_t.StatusCode.ERROR, str(e))
            span.record_exception(e)

            # Still track the failed attempt
            tasks = tool_context.state.get("app:TASKS_PERFORMED") or []
            tasks.append({
                "OPERATION_STATUS": "FAILED",
                "GENERATED_QUERY": query,
                "ERROR_STATUS": str(e),
            })
            tool_context.state["app:TASKS_PERFORMED"] = tasks

            return {
                "success": False,
                "query": query,
                "error": str(e),
                "message": f"Query execution failed: {str(e)}",
            }


def register_copy_into_query(query: str, table: str, tool_context: ToolContext) -> dict:
    """
    Register a COPY INTO query in the session state under app:TASKS_PERFORMED.

    Call this tool after generating a COPY INTO query intended for Snowpipe use,
    so that the Snowpipe Specialist can later retrieve it from session state.

    Args:
        query: The complete COPY INTO SQL statement.
        table: The fully-qualified target table name (e.g. DATABASE.SCHEMA.TABLE).
        tool_context: ADK tool context carrying session state.

    Returns:
        A dictionary with ``success`` (bool) and a confirmation message.
    """
    try:
        logger_name = tool_context.state.get("app:LOGGER")
        logger = logging.getLogger(logger_name).getChild(__name__) if logger_name else logging.getLogger(__name__)
        logger.info("register_copy_into_query: table=%s query=%s", table, query[:200])

        tasks = tool_context.state.get("app:TASKS_PERFORMED") or []
        tasks.append({
            "OPERATION_TYPE": "COPY_INTO",
            "TARGET_TABLE": table.upper(),
            "GENERATED_QUERY": query,
            "OPERATION_STATUS": "REGISTERED",
        })
        tool_context.state["app:TASKS_PERFORMED"] = tasks

        logger.debug("register_copy_into_query: registered entry, total tasks=%d", len(tasks))
        return {
            "success": True,
            "table": table,
            "query": query,
            "message": f"COPY INTO query for table '{table}' registered in session state.",
        }
    except Exception as e:
        logging.getLogger(__name__).exception("Error registering copy into query")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to register COPY INTO query: {str(e)}",
        }


def get_session_state(tool_context: ToolContext) -> dict:
    """
    Retrieve the current app state variables for the active session.

    This tool reads the session state and returns:
    - tasks_performed: list of all tasks/operations completed so far (app:TASKS_PERFORMED)
    - queries_executed: list of all SQL queries executed in this session (user:QUERIES_EXECUTED)
    - account_identifier: the Snowflake account being used (app:ACCOUNT_IDENTIFIER)
    - auto_generate_comments: whether auto-comment generation is enabled (app:AUTO_GENERATE_COMMENTS)

    Use this tool when the user asks questions like:
    - "what have you done so far?"
    - "show me the tasks performed"
    - "what queries were executed?"
    - "give me a summary of operations in this session"
    - "what has been completed?"

    Args:
        tool_context: ADK tool context containing the session state

    Returns:
        Dictionary with tasks_performed, queries_executed, and other session state variables
    """
    try:
        logger_name = tool_context.state.get("app:LOGGER")
        logger = logging.getLogger(logger_name).getChild(__name__)
        tasks_performed = tool_context.state.get("app:TASKS_PERFORMED") or []
        queries_executed = tool_context.state.get("user:QUERIES_EXECUTED") or []
        account_identifier = tool_context.state.get("app:ACCOUNT_IDENTIFIER") or ""
        auto_generate_comments = tool_context.state.get("app:AUTO_GENERATE_COMMENTS") or ""

        return {
            "success": True,
            "tasks_performed": tasks_performed,
            "tasks_performed_count": len(tasks_performed),
            "queries_executed": queries_executed,
            "queries_executed_count": len(queries_executed),
            "account_identifier": account_identifier,
            "auto_generate_comments": auto_generate_comments,
        }
    except Exception as e:
        logging.getLogger(__name__).exception("Error retrieving session state")
        return {
            "success": False,
            "tasks_performed": [],
            "tasks_performed_count": 0,
            "queries_executed": [],
            "queries_executed_count": 0,
            "account_identifier": "",
            "auto_generate_comments": "",
            "error": str(e),
            "message": f"Error retrieving session state: {str(e)}",
        }


def get_research_results(object_type: str, tool_context: ToolContext) -> dict:
    """
    Retrieve cached research results for a given Snowflake object type from the
    shared session state (``app:RESEARCH_RESULTS``).

    Call this tool BEFORE invoking the RESEARCH_AGENT.  If a non-empty result is
    returned the agent should use it directly and skip the web search.

    Args:
        object_type: The Snowflake object type to look up (e.g. ``"TABLE"``,
            ``"STREAM"``, ``"WAREHOUSE"``).  Case-insensitive.
        tool_context: ADK tool context carrying the shared session state.

    Returns:
        A dictionary with ``found`` (bool), ``object_type`` (str), and ``results``
        (the cached research text, or an empty string when not found).
    """
    logger = logging.getLogger(__name__)
    try:
        key = object_type.strip().upper()
        research_results: dict = tool_context.state.get("app:RESEARCH_RESULTS") or {}
        results = research_results.get(key, "")
        found = bool(results)
        logger.debug("get_research_results: object_type=%s found=%s", key, found)
        return {
            "found": found,
            "object_type": key,
            "results": results,
        }
    except Exception as e:
        logger.exception("get_research_results: error reading state")
        return {
            "found": False,
            "object_type": object_type,
            "results": "",
            "error": str(e),
        }
