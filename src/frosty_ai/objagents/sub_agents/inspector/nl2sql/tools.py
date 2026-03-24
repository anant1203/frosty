import logging
import pathlib
import re
import textwrap
from typing import Any

from google.adk.tools import ToolContext
from src.session import Session

_ALLOWED_PREFIXES = re.compile(
    r"^\s*(--[^\n]*\n\s*)*(SELECT|WITH|SHOW|DESCRIBE|DESC)\b",
    re.IGNORECASE,
)


def _get_session(tool_context: ToolContext):
    """Build a Snowflake Snowpark session from ADK ToolContext state."""
    session_inst = Session()
    session_inst.set_user(tool_context.state.get("user:SNOWFLAKE_USER_NAME"))
    session_inst.set_account(tool_context.state.get("app:ACCOUNT_IDENTIFIER"))
    session_inst.set_password(tool_context.state.get("user:USER_PASSWORD"))
    if tool_context.state.get("user:AUTHENTICATOR"):
        session_inst.set_authenticator(tool_context.state.get("user:AUTHENTICATOR"))
    if tool_context.state.get("user:ROLE"):
        session_inst.set_role(tool_context.state.get("user:ROLE"))
    if tool_context.state.get("app:WAREHOUSE"):
        session_inst.set_warehouse(tool_context.state.get("app:WAREHOUSE"))
    if tool_context.state.get("app:DATABASE"):
        session_inst.set_database(tool_context.state.get("app:DATABASE"))
    return session_inst.get_session()


def discover_schema(
    database: str,
    schema: str,
    tool_context: ToolContext,
) -> dict:
    """
    Fetch all tables and their columns from a Snowflake schema in a single
    query — providing the schema context needed to generate accurate SQL.

    Joins INFORMATION_SCHEMA.COLUMNS with INFORMATION_SCHEMA.TABLES to return
    table-level metadata (type, row count, comment) alongside column details
    (name, data type, nullability, comment) for every table in the schema.

    Args:
        database: Snowflake database name (e.g. MY_DB).
        schema:   Schema name (e.g. SALES).
        tool_context: ADK tool context carrying session credentials.

    Returns:
        Dict with ``success``, ``database``, ``schema``, ``tables`` (a dict
        keyed by table name, each with table_type, row_count, and columns list),
        ``table_count``, and ``message``.
    """
    logger_name = tool_context.state.get("app:LOGGER")
    log = logging.getLogger(logger_name).getChild(__name__) if logger_name else logging.getLogger(__name__)
    log.info("discover_schema: %s.%s", database, schema)

    try:
        session = _get_session(tool_context)

        sql = f"""
            SELECT
                c.TABLE_NAME,
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.IS_NULLABLE,
                c.COLUMN_DEFAULT,
                c.ORDINAL_POSITION,
                t.TABLE_TYPE,
                t.ROW_COUNT,
                t.COMMENT  AS TABLE_COMMENT,
                c.COMMENT  AS COLUMN_COMMENT
            FROM {database}.INFORMATION_SCHEMA.COLUMNS  c
            JOIN {database}.INFORMATION_SCHEMA.TABLES   t
              ON  c.TABLE_SCHEMA = t.TABLE_SCHEMA
             AND  c.TABLE_NAME   = t.TABLE_NAME
            WHERE c.TABLE_SCHEMA = '{schema.upper()}'
            ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION
        """
        rows = session.sql(sql).collect()

        tables: dict[str, Any] = {}
        for r in rows:
            tname = r["TABLE_NAME"]
            if tname not in tables:
                tables[tname] = {
                    "table_type": r["TABLE_TYPE"],
                    "row_count": r["ROW_COUNT"],
                    "comment": r["TABLE_COMMENT"],
                    "columns": [],
                }
            tables[tname]["columns"].append({
                "name": r["COLUMN_NAME"],
                "type": r["DATA_TYPE"],
                "nullable": r["IS_NULLABLE"],
                "default": r["COLUMN_DEFAULT"],
                "comment": r["COLUMN_COMMENT"],
            })

        total_columns = sum(len(t["columns"]) for t in tables.values())

        return {
            "success": True,
            "database": database,
            "schema": schema,
            "tables": tables,
            "table_count": len(tables),
            "message": (
                f"Found {len(tables)} tables with {total_columns} total columns "
                f"in {database}.{schema}."
            ),
        }

    except Exception as e:
        log.exception("discover_schema failed")
        return {
            "success": False,
            "database": database,
            "schema": schema,
            "error": str(e),
            "message": f"Failed to discover schema {database}.{schema}: {e}",
        }


def run_data_query(sql: str, tool_context: ToolContext) -> dict:
    """
    Execute a read-only SQL query against Snowflake and return the results.

    Only SELECT, WITH (CTEs), SHOW, and DESCRIBE statements are permitted.
    Any attempt to run INSERT, UPDATE, DELETE, DROP, CREATE, TRUNCATE, or other
    write/DDL statements is rejected before reaching Snowflake.

    Args:
        sql:          The SQL statement to execute (must be read-only).
        tool_context: ADK tool context carrying session credentials.

    Returns:
        Dict with ``success``, ``sql``, ``rows`` (list of dicts), ``row_count``,
        and ``message``. On rejection or error, returns ``success: False`` with
        an ``error`` field describing the problem.
    """
    logger_name = tool_context.state.get("app:LOGGER")
    log = logging.getLogger(logger_name).getChild(__name__) if logger_name else logging.getLogger(__name__)

    # ── Safety gate: only allow read-only statements ─────────────────────────
    if not _ALLOWED_PREFIXES.match(sql):
        log.warning("run_data_query: rejected non-SELECT statement")
        return {
            "success": False,
            "sql": sql,
            "error": "Only SELECT, WITH, SHOW, and DESCRIBE statements are permitted.",
            "message": (
                "This tool is read-only. The provided SQL was rejected because it "
                "does not start with SELECT, WITH, SHOW, or DESCRIBE. Please rewrite "
                "it as a SELECT query."
            ),
        }

    log.info("run_data_query: %s", sql[:200])

    try:
        session = _get_session(tool_context)
        result_rows = session.sql(sql).collect()
        rows = [
            r.as_dict() if hasattr(r, "as_dict") else dict(r)
            for r in result_rows
        ]

        return {
            "success": True,
            "sql": sql,
            "rows": rows,
            "row_count": len(rows),
            "message": f"Query returned {len(rows):,} row(s).",
        }

    except Exception as e:
        log.exception("run_data_query failed")
        return {
            "success": False,
            "sql": sql,
            "error": str(e),
            "message": f"Query execution failed: {e}",
        }


# ── Keyword sets for heuristic inference ────────────────────────────────────
_METRIC_KEYWORDS = {
    "VALUE", "AMOUNT", "REVENUE", "COST", "PRICE", "TOTAL", "COUNT",
    "QTY", "QUANTITY", "SALES", "PROFIT", "MARGIN", "SPEND", "BUDGET",
    "FEE", "RATE", "SCORE", "WEIGHT",
}
_DATE_KEYWORDS = {"DATE", "AT", "TIME", "TS", "TIMESTAMP", "DAY", "WEEK", "MONTH", "YEAR"}
_ENUM_KEYWORDS = {"STATUS", "TYPE", "STATE", "FLAG", "CATEGORY", "KIND", "MODE", "STAGE"}
_NUMERIC_TYPES_DRAFT = {
    "NUMBER", "DECIMAL", "NUMERIC", "INT", "INTEGER", "BIGINT", "SMALLINT",
    "FLOAT", "FLOAT4", "FLOAT8", "DOUBLE", "REAL", "FIXED",
}
_DATE_TYPES = {"DATE", "TIMESTAMP", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ", "DATETIME", "TIME"}


def _col_contains(name: str, keywords: set[str]) -> bool:
    """Return True if any keyword appears as a word-boundary segment in name."""
    parts = set(re.split(r"[_\s]", name.upper()))
    return bool(parts & keywords)


def generate_business_rules_draft(
    database: str,
    schema: str,
    tool_context: ToolContext,
) -> dict:
    """
    Inspect a Snowflake schema and write a first-draft business-rules.md to the
    snowflake-data-analyst skill, pre-populated with candidates inferred from
    column names and data types.

    Analyses:
    - Metric candidates — numeric columns whose names suggest measures
      (e.g. ORDER_VALUE, TOTAL_REVENUE, UNIT_COST).
    - Date column candidates — date/timestamp columns per table, highlighting
      the most likely "primary" date (prefers *_DATE over CREATED_AT/UPDATED_AT).
    - Enum/status candidates — varchar columns whose names suggest categorical
      values that may need standard filters (e.g. STATUS, ORDER_TYPE).
    - Join key candidates — columns ending in _ID that appear in multiple tables,
      suggesting foreign-key relationships.

    The draft is written directly to
    ``skills/snowflake-data-analyst/references/business-rules.md`` so the user
    can open it, review the inferred candidates, and replace placeholders with
    their real business definitions.

    Args:
        database: Snowflake database name (e.g. MY_DB).
        schema:   Schema name (e.g. SALES).
        tool_context: ADK tool context carrying session credentials.

    Returns:
        Dict with ``success``, ``path``, ``tables_analysed``,
        ``metric_candidates``, ``date_candidates``, and ``message``.
    """
    logger_name = tool_context.state.get("app:LOGGER")
    log = (
        logging.getLogger(logger_name).getChild(__name__)
        if logger_name
        else logging.getLogger(__name__)
    )
    log.info("generate_business_rules_draft: %s.%s", database, schema)

    try:
        session = _get_session(tool_context)

        sql = f"""
            SELECT
                c.TABLE_NAME,
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.IS_NULLABLE,
                c.ORDINAL_POSITION,
                t.ROW_COUNT,
                c.COMMENT AS COLUMN_COMMENT
            FROM {database}.INFORMATION_SCHEMA.COLUMNS  c
            JOIN {database}.INFORMATION_SCHEMA.TABLES   t
              ON  c.TABLE_SCHEMA = t.TABLE_SCHEMA
             AND  c.TABLE_NAME   = t.TABLE_NAME
            WHERE c.TABLE_SCHEMA = '{schema.upper()}'
            ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION
        """
        rows = session.sql(sql).collect()

        if not rows:
            return {
                "success": False,
                "database": database,
                "schema": schema,
                "message": f"No columns found in {database}.{schema}. Check the database and schema names.",
            }

        # ── Organise columns by table ────────────────────────────────────────
        tables: dict[str, list[dict]] = {}
        for r in rows:
            tname = r["TABLE_NAME"]
            if tname not in tables:
                tables[tname] = []
            tables[tname].append({
                "name": r["COLUMN_NAME"],
                "type": r["DATA_TYPE"].upper().split("(")[0].strip(),
                "nullable": r["IS_NULLABLE"],
                "comment": r["COLUMN_COMMENT"] or "",
            })

        # ── Heuristic analysis ───────────────────────────────────────────────
        metric_candidates: list[dict] = []   # {table, column, type}
        date_candidates: list[dict] = []     # {table, column, primary}
        enum_candidates: list[dict] = []     # {table, column}
        id_columns: dict[str, list[str]] = {}  # col_name → [tables]

        for tname, cols in tables.items():
            table_dates = []
            for col in cols:
                cname = col["name"]
                ctype = col["type"]

                # Metric: numeric type AND name suggests a measure
                if ctype in _NUMERIC_TYPES_DRAFT and _col_contains(cname, _METRIC_KEYWORDS):
                    metric_candidates.append({"table": tname, "column": cname, "type": ctype})

                # Date column
                if ctype in _DATE_TYPES:
                    is_primary = _col_contains(cname, {"DATE"}) and not _col_contains(
                        cname, {"CREATED", "UPDATED", "MODIFIED", "DELETED"}
                    )
                    table_dates.append({"table": tname, "column": cname, "primary": is_primary})

                # Enum/status
                if ctype in {"VARCHAR", "TEXT", "STRING", "CHAR"} and _col_contains(cname, _ENUM_KEYWORDS):
                    enum_candidates.append({"table": tname, "column": cname})

                # Join key candidate
                if cname.upper().endswith("_ID"):
                    id_columns.setdefault(cname.upper(), []).append(tname)

            # Sort: primary dates first
            table_dates.sort(key=lambda d: (not d["primary"], d["column"]))
            date_candidates.extend(table_dates)

        # FK candidates: _ID columns appearing in 2+ tables
        fk_candidates = {col: tbls for col, tbls in id_columns.items() if len(tbls) >= 2}

        # ── Build draft Markdown ─────────────────────────────────────────────
        def _metric_lines() -> str:
            if not metric_candidates:
                return "<!-- No numeric measure columns detected. Add your metric definitions here. -->\n"
            lines = ["<!-- Inferred from column names and types. Replace with your actual definitions. -->\n"]
            for m in metric_candidates:
                hint = f"SUM({m['table']}.{m['column']})"
                lines.append(f"<!-- - **{m['column']}** ({m['table']}): {hint} [add WHERE filters if needed] -->")
            return "\n".join(lines)

        def _date_lines() -> str:
            if not date_candidates:
                return "<!-- No date/timestamp columns detected. Add your canonical date columns here. -->\n"
            seen_tables: set[str] = set()
            lines = ["<!-- Inferred from DATE/TIMESTAMP columns. Mark the primary date per table. -->\n"]
            for d in date_candidates:
                if d["table"] not in seen_tables:
                    marker = " ← recommended primary" if d["primary"] else ""
                    lines.append(f"<!-- - {d['table']}: use {d['column']}{marker} -->")
                    seen_tables.add(d["table"])
                else:
                    lines.append(f"<!-- - {d['table']} (alternative): {d['column']} -->")
            return "\n".join(lines)

        def _filter_lines() -> str:
            if not enum_candidates:
                return "<!-- No status/type columns detected. Add always-on filters here. -->\n"
            lines = ["<!-- Inferred status/categorical columns — add standard filters below. -->\n"]
            for e in enum_candidates:
                lines.append(f"<!-- - {e['table']}.{e['column']}: WHERE {e['column']} = '?' -->")
            return "\n".join(lines)

        def _join_lines() -> str:
            if not fk_candidates:
                return "<!-- No shared _ID columns detected. Add your join keys here. -->\n"
            lines = ["<!-- Inferred from _ID columns appearing in multiple tables. Verify join direction. -->\n"]
            for col, tbls in fk_candidates.items():
                for i in range(len(tbls) - 1):
                    lines.append(
                        f"<!-- - {tbls[i]} → {tbls[i+1]}: "
                        f"JOIN ON {tbls[i]}.{col} = {tbls[i+1]}.{col} -->"
                    )
            return "\n".join(lines)

        draft = textwrap.dedent(f"""\
            # Business Rules for DATA_ANALYST
            # Auto-generated draft for {database}.{schema}
            # Review each section and replace placeholder comments with your real definitions.

            ---

            ## Metric Definitions

            Define what each business term means in SQL terms.

            {_metric_lines()}

            ---

            ## Canonical Date Columns

            Specify which date column to use for time-based filters per table.

            {_date_lines()}

            ---

            ## Standard Filters

            Filters applied to every query on a table unless the user says otherwise.

            {_filter_lines()}

            ---

            ## Common Table Joins

            Canonical join keys between tables.

            {_join_lines()}

            ---

            ## Column Aliases / Semantic Mappings

            Map plain-English terms to actual columns or expressions.

            <!-- Examples:
            - "revenue" → SUM(ORDER_VALUE) WHERE STATUS = 'COMPLETED'
            - "headcount" → COUNT(DISTINCT EMPLOYEE_ID) in HR_EMPLOYEES
            -->

            ---

            ## Business Calendar Rules

            Non-standard date or period logic.

            <!-- Examples:
            - Fiscal year starts February 1
            - "Last quarter" means the previous fiscal quarter
            -->
        """)

        # ── Write file ───────────────────────────────────────────────────────
        out_path = (
            pathlib.Path(__file__).parents[6]
            / "skills"
            / "snowflake-data-analyst"
            / "references"
            / "business-rules.md"
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(draft, encoding="utf-8")

        log.info("generate_business_rules_draft: wrote %s", out_path)

        return {
            "success": True,
            "path": str(out_path),
            "tables_analysed": len(tables),
            "metric_candidates": [f"{m['table']}.{m['column']}" for m in metric_candidates],
            "date_candidates": [f"{d['table']}.{d['column']}" for d in date_candidates],
            "enum_candidates": [f"{e['table']}.{e['column']}" for e in enum_candidates],
            "join_candidates": [
                f"{tbls[0]}.{col} → {tbls[1]}.{col}"
                for col, tbls in fk_candidates.items()
                for _ in [None]
            ],
            "message": (
                f"Draft written to {out_path}. "
                f"Open the file, review the {len(metric_candidates)} metric candidate(s), "
                f"{len(date_candidates)} date column(s), and {len(fk_candidates)} join key(s), "
                f"then replace the placeholder comments with your actual business definitions."
            ),
        }

    except Exception as e:
        log.exception("generate_business_rules_draft failed")
        return {
            "success": False,
            "database": database,
            "schema": schema,
            "error": str(e),
            "message": f"Failed to generate business rules draft: {e}",
        }
