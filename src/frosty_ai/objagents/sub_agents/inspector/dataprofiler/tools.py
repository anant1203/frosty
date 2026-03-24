import logging
from typing import Any

from google.adk.tools import ToolContext
from src.session import Session

_NUMERIC_TYPES = {
    "NUMBER", "DECIMAL", "NUMERIC", "INT", "INTEGER", "BIGINT", "SMALLINT",
    "TINYINT", "BYTEINT", "FLOAT", "FLOAT4", "FLOAT8", "DOUBLE",
    "DOUBLE PRECISION", "REAL", "FIXED",
}


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


def _cardinality_label(distinct: int, total: int) -> str:
    if total == 0:
        return "unknown"
    ratio = distinct / total
    if distinct <= 1:
        return "constant"
    if distinct < 50 or ratio < 0.1:
        return "low"
    if ratio > 0.9:
        return "high"
    return "medium"


def profile_table(
    database: str,
    schema: str,
    table: str,
    tool_context: ToolContext,
) -> dict:
    """
    Run a comprehensive statistical profile on a Snowflake table.

    Executes two queries:
    1. Fetch column metadata from INFORMATION_SCHEMA.COLUMNS.
    2. A single dynamic SQL pass that computes per-column: row count, null count,
       null %, distinct count, min, max, and (for numeric columns) avg, stddev,
       and 25th/50th/75th percentiles.

    Args:
        database: Snowflake database name (e.g. MY_DB).
        schema:   Schema name (e.g. SALES).
        table:    Table name (e.g. ORDERS).
        tool_context: ADK tool context carrying session credentials.

    Returns:
        Dict with ``success``, ``table``, ``total_rows``, ``columns`` list, and
        ``message``. Each column entry contains name, data_type, null_count,
        null_pct, distinct_count, cardinality, min, max, and optionally avg,
        stddev, p25, p50, p75 for numeric types.
    """
    logger_name = tool_context.state.get("app:LOGGER")
    log = logging.getLogger(logger_name).getChild(__name__) if logger_name else logging.getLogger(__name__)
    log.info("profile_table: %s.%s.%s", database, schema, table)

    try:
        session = _get_session(tool_context)

        # ── Step 1: column metadata ──────────────────────────────────────────
        meta_sql = f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
            FROM {database}.INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{schema.upper()}'
              AND TABLE_NAME   = '{table.upper()}'
            ORDER BY ORDINAL_POSITION
        """
        meta_rows = session.sql(meta_sql).collect()

        if not meta_rows:
            return {
                "success": False,
                "table": f"{database}.{schema}.{table}",
                "message": f"Table {database}.{schema}.{table} not found or has no columns.",
            }

        col_meta: list[dict[str, Any]] = [
            {
                "name": r["COLUMN_NAME"],
                "data_type": r["DATA_TYPE"],
                "nullable": r["IS_NULLABLE"] == "YES",
            }
            for r in meta_rows
        ]

        # ── Step 2: dynamic single-pass profile query ────────────────────────
        parts = ["COUNT(*) AS __TOTAL_ROWS__"]

        for col in col_meta:
            c = col["name"]
            cq = f'"{c}"'  # quoted identifier
            alias = c.replace('"', "").replace(" ", "_")
            is_numeric = col["data_type"].upper().split("(")[0].strip() in _NUMERIC_TYPES

            parts.append(f"COUNT({cq}) AS \"{alias}__non_null\"")
            parts.append(f"(COUNT(*) - COUNT({cq})) AS \"{alias}__null_count\"")
            parts.append(
                f"ROUND((COUNT(*) - COUNT({cq})) * 100.0 / NULLIF(COUNT(*), 0), 2)"
                f" AS \"{alias}__null_pct\""
            )
            parts.append(f"COUNT(DISTINCT {cq}) AS \"{alias}__distinct\"")
            parts.append(f"MIN({cq}) AS \"{alias}__min\"")
            parts.append(f"MAX({cq}) AS \"{alias}__max\"")

            if is_numeric:
                # Numeric columns are already the right type — cast directly.
                # TRY_TO_DOUBLE raises a SQL compilation error when the source
                # type is already NUMBER/FLOAT, so we avoid it here.
                parts.append(
                    f"ROUND(AVG({cq}::FLOAT), 4) AS \"{alias}__avg\""
                )
                parts.append(
                    f"ROUND(STDDEV({cq}::FLOAT), 4) AS \"{alias}__stddev\""
                )
                parts.append(
                    f"PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY {cq}::FLOAT)"
                    f" AS \"{alias}__p25\""
                )
                parts.append(
                    f"PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY {cq}::FLOAT)"
                    f" AS \"{alias}__p50\""
                )
                parts.append(
                    f"PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY {cq}::FLOAT)"
                    f" AS \"{alias}__p75\""
                )

        profile_sql = (
            f"SELECT {', '.join(parts)}\n"
            f"FROM {database}.{schema}.\"{table.upper()}\""
        )
        log.debug("profile_sql: %s", profile_sql[:500])
        profile_row = session.sql(profile_sql).collect()[0].as_dict()

        total_rows = int(profile_row.get("__TOTAL_ROWS__", 0))

        # ── Build structured column results ─────────────────────────────────
        columns_out = []
        for col in col_meta:
            c = col["name"]
            alias = c.replace('"', "").replace(" ", "_")
            is_numeric = col["data_type"].upper().split("(")[0].strip() in _NUMERIC_TYPES

            null_count = int(profile_row.get(f"{alias}__null_count", 0) or 0)
            null_pct = float(profile_row.get(f"{alias}__null_pct", 0.0) or 0.0)
            distinct = int(profile_row.get(f"{alias}__distinct", 0) or 0)

            entry: dict[str, Any] = {
                "name": c,
                "data_type": col["data_type"],
                "nullable": col["nullable"],
                "null_count": null_count,
                "null_pct": null_pct,
                "distinct_count": distinct,
                "cardinality": _cardinality_label(distinct, total_rows),
                "min": profile_row.get(f"{alias}__min"),
                "max": profile_row.get(f"{alias}__max"),
            }

            if is_numeric:
                entry["avg"] = profile_row.get(f"{alias}__avg")
                entry["stddev"] = profile_row.get(f"{alias}__stddev")
                entry["p25"] = profile_row.get(f"{alias}__p25")
                entry["p50"] = profile_row.get(f"{alias}__p50")
                entry["p75"] = profile_row.get(f"{alias}__p75")

            columns_out.append(entry)

        return {
            "success": True,
            "table": f"{database}.{schema}.{table}",
            "total_rows": total_rows,
            "column_count": len(columns_out),
            "columns": columns_out,
            "message": (
                f"Profiled {len(columns_out)} columns across "
                f"{total_rows:,} rows in {database}.{schema}.{table}."
            ),
        }

    except Exception as e:
        log.exception("profile_table failed")
        return {
            "success": False,
            "table": f"{database}.{schema}.{table}",
            "error": str(e),
            "message": f"Failed to profile table: {e}",
        }


def get_top_values(
    database: str,
    schema: str,
    table: str,
    column: str,
    limit: int,
    tool_context: ToolContext,
) -> dict:
    """
    Return the top N most frequent values for a column in a Snowflake table.

    Best used for low-cardinality columns (e.g. STATUS, REGION, TYPE) to
    understand the value distribution at a glance.

    Args:
        database: Snowflake database name.
        schema:   Schema name.
        table:    Table name.
        column:   Column to analyse.
        limit:    Number of top values to return (default 10, max 50).
        tool_context: ADK tool context carrying session credentials.

    Returns:
        Dict with ``success``, ``column``, ``top_values`` (list of
        {value, frequency, pct}), and ``message``.
    """
    logger_name = tool_context.state.get("app:LOGGER")
    log = logging.getLogger(logger_name).getChild(__name__) if logger_name else logging.getLogger(__name__)
    log.info("get_top_values: %s.%s.%s.%s limit=%d", database, schema, table, column, limit)

    try:
        limit = min(max(1, limit), 50)
        session = _get_session(tool_context)

        sql = f"""
            SELECT
                "{column}" AS VALUE,
                COUNT(*) AS FREQUENCY,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS PCT
            FROM {database}.{schema}."{table.upper()}"
            GROUP BY "{column}"
            ORDER BY FREQUENCY DESC
            LIMIT {limit}
        """
        rows = session.sql(sql).collect()
        top_values = [
            {
                "value": str(r["VALUE"]) if r["VALUE"] is not None else None,
                "frequency": int(r["FREQUENCY"]),
                "pct": float(r["PCT"]),
            }
            for r in rows
        ]

        return {
            "success": True,
            "column": column,
            "top_values": top_values,
            "message": f"Top {len(top_values)} values for column '{column}'.",
        }

    except Exception as e:
        log.exception("get_top_values failed")
        return {
            "success": False,
            "column": column,
            "error": str(e),
            "message": f"Failed to get top values for column '{column}': {e}",
        }
