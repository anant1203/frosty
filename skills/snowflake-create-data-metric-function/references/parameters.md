# CREATE DATA METRIC FUNCTION — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-data-metric-function

---

## Full Syntax

```sql
CREATE [ OR REPLACE ] [ SECURE ] DATA METRIC FUNCTION [ IF NOT EXISTS ] <name>
  ( <table_arg> TABLE( <col_arg> <data_type> [ , <col_arg> <data_type> ... ] )
    [ , <table_arg> TABLE( <col_arg> <data_type> [ , ... ] ) ] )
  RETURNS NUMBER [ [ NOT ] NULL ]
  [ LANGUAGE SQL ]
  [ COMMENT = '<string_literal>' ]
  AS
  '<expression>'
```

### CREATE OR ALTER Variant (Preview)

```sql
CREATE [ OR ALTER ] DATA METRIC FUNCTION <name>
  ( <table_arg> TABLE( <col_arg> <data_type> [ , ... ] ) )
  RETURNS NUMBER
  [ LANGUAGE SQL ]
  [ COMMENT = '<string_literal>' ]
  AS
  '<expression>'
```

---

## Defaults Table

| Parameter | Default Value |
|---|---|
| `OR REPLACE` | Not set (error if DMF already exists) |
| `SECURE` | Not set (definition visible to authorized users) |
| `IF NOT EXISTS` | Not set |
| `RETURNS NUMBER NULL / NOT NULL` | `NULL` (function may return NULL) |
| `LANGUAGE` | `SQL` (only supported value) |
| `COMMENT` | None |

---

## Parameter Descriptions

### `name`
Identifier for the Data Metric Function. Must be unique within the schema. Must start with an alphabetic character. Use double-quoted identifiers for names containing special characters or spaces.

### `table_arg TABLE( col_arg data_type [, ...] )`
**Required.** Defines the function signature. `table_arg` is the name used to reference the table argument inside the function body. Each `col_arg data_type` pair declares a column that the expression may reference; all declared columns must belong to the same physical table when the DMF is applied. Multiple `TABLE(...)` argument groups may be specified. At least one column argument is required per table argument.

### `RETURNS NUMBER`
**Required.** The return type is always `NUMBER`. Data Metric Functions must return a scalar numeric value (typically a count, ratio, or flag: 0 = pass, 1 = fail, or a custom quality score).

### `NOT NULL`
Asserts that the function never returns NULL. This is informational — Snowflake does not enforce it at runtime.

### `OR REPLACE`
Atomically replaces an existing DMF with the same name and signature. Mutually exclusive with `IF NOT EXISTS`. Prefer `IF NOT EXISTS` in idempotent DDL.

### `SECURE`
Hides the function definition and expression body from non-owner roles. Use when the quality check logic or column names reveal sensitive business rules.

### `IF NOT EXISTS`
Creates the DMF only if no DMF with the same name already exists. Mutually exclusive with `OR REPLACE`.

### `LANGUAGE SQL`
Specifies that the expression is written in SQL. Currently the only supported language for DMFs. Can be omitted — SQL is the implicit default.

### `COMMENT`
Optional free-text description of the metric. Visible in `SHOW DATA METRIC FUNCTIONS` and `DESCRIBE DATA METRIC FUNCTION`.

### `AS '<expression>'`
**Required.** The SQL expression body. Rules and restrictions:
- Must return a scalar NUMBER value.
- Must be deterministic — avoid nondeterministic functions such as `CURRENT_TIME()`, `RANDOM()`, `UUID_STRING()`.
- Supports `WITH` (CTE) and `WHERE` clauses.
- Cannot reference objects that depend on UDFs or UDTFs.
- Cannot use nonscalar return values (no subqueries returning multiple rows without aggregation).
- Use `$$` as the delimiter to avoid escaping internal single quotes.
- Reference declared column arguments by `table_arg.col_arg` syntax.

---

## Usage Notes

- DMFs are applied to tables and views via `ALTER TABLE ... ADD DATA METRIC FUNCTION` or `ALTER VIEW ...`.
- The quality measurement schedule is controlled at the table/view level via `DATA_METRIC_SCHEDULE`.
- DMF results are stored in `SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS` (Snowflake-hosted) or a custom results table.
- Only SQL is supported as the expression language; Python, Java, and JavaScript are not available for DMFs.
- The `OR ALTER` variant (preview) allows modifying an existing DMF's body, RUNTIME settings, PACKAGES, and COMMENT without dropping and recreating it.
