# Snowflake CREATE TABLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-table

---

## Full Syntax

### Standard CREATE TABLE

```sql
CREATE [ OR REPLACE ]
    [ { [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE | TRANSIENT } ]
  TABLE [ IF NOT EXISTS ] <table_name>
  (
    <col_name> <col_type>
      [ inlineConstraint ]
      [ NOT NULL ]
      [ COLLATE '<collation_specification>' ]
      [ DEFAULT <expr> | { AUTOINCREMENT | IDENTITY } [ ( <seed> , <step> ) ] [ { ORDER | NOORDER } ] ]
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col1>, <cond_col1>, ... ) ] ]
      [ [ WITH ] PROJECTION POLICY <policy_name> ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
      [ COMMENT '<string_literal>' ]
    [ , <col_name> <col_type> [ ... ] ]
    [ , outoflineConstraint [ ... ] ]
  )
  [ CLUSTER BY ( <expr> [ , ... ] ) ]
  [ ENABLE_SCHEMA_EVOLUTION = { TRUE | FALSE } ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ COPY GRANTS ]
  [ COPY TAGS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , ... ] ) ] ]
  [ [ WITH ] JOIN POLICY <policy_name> [ ALLOWED JOIN KEYS ( <col_name> [ , ... ] ) ] ]
  [ [ WITH ] STORAGE LIFECYCLE POLICY <policy_name> ON ( <col_name> [ , ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , ... ] ) ]
  [ ROW_TIMESTAMP = { TRUE | FALSE } ]
```

### CREATE TABLE … AS SELECT (CTAS)

```sql
CREATE [ OR REPLACE ] TABLE <table_name> [ ( <col_name> [ , ... ] ) ]
  [ CLUSTER BY ( <expr> [ , ... ] ) ]
  [ COPY GRANTS ]
  [ COPY TAGS ]
  AS <query>
```

### CREATE TABLE … LIKE

```sql
CREATE [ OR REPLACE ] TABLE <table_name> LIKE <source_table>
  [ CLUSTER BY ( <expr> [ , ... ] ) ]
  [ COPY GRANTS ]
```

Copies the column definitions of an existing table without copying any data.

### CREATE TABLE … CLONE

```sql
CREATE [ OR REPLACE ]
    [ { [ { LOCAL | GLOBAL } ] TEMP [ READ ONLY ] | TEMPORARY [ READ ONLY ] | VOLATILE | TRANSIENT } ]
  TABLE <name> CLONE <source_table>
    [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
    [ COPY GRANTS ]
```

Creates a zero-copy clone. The optional `AT | BEFORE` clause enables point-in-time cloning via Time Travel.

### CREATE TABLE … USING TEMPLATE

```sql
CREATE [ OR REPLACE ] TABLE <table_name>
  [ COPY GRANTS ]
  USING TEMPLATE <query>
```

Derives column definitions automatically from staged files using the `INFER_SCHEMA` function.

### CREATE TABLE … FROM ARCHIVE OF

```sql
CREATE [ TRANSIENT ] TABLE [ IF NOT EXISTS ] <name>
  FROM ARCHIVE OF <source_table> [ [ AS ] <alias_name> ]
  WHERE <expression>
```

### CREATE TABLE … FROM BACKUP SET

```sql
CREATE TABLE <name> FROM BACKUP SET <backup_set> IDENTIFIER '<backup_id>'
```

---

## Defaults Table

| Parameter | Default |
|-----------|---------|
| Table type (TEMP / TRANSIENT / VOLATILE) | Permanent |
| NOT NULL | NULL allowed |
| DEFAULT / AUTOINCREMENT | No default; AUTOINCREMENT starts at 1, increments by 1 |
| CLUSTER BY | None |
| ENABLE_SCHEMA_EVOLUTION | FALSE |
| DATA_RETENTION_TIME_IN_DAYS | 1 (Standard: 0–1; Enterprise: 0–90) |
| MAX_DATA_EXTENSION_TIME_IN_DAYS | 14 |
| CHANGE_TRACKING | FALSE |
| DEFAULT_DDL_COLLATION | None (session/account default applies) |
| COPY GRANTS | Not applied |
| COPY TAGS | Not applied |
| COMMENT | None |
| ROW ACCESS POLICY | None |
| AGGREGATION POLICY | None |
| JOIN POLICY | None |
| STORAGE LIFECYCLE POLICY | None |
| MASKING POLICY (column) | None |
| PROJECTION POLICY (column) | None |
| ROW_TIMESTAMP | FALSE |

---

## Parameter Descriptions

### Table-type modifiers (mutually exclusive with each other)

| Keyword | Description |
|---------|-------------|
| `TEMPORARY` / `TEMP` / `VOLATILE` | Session-scoped table — automatically dropped when the session ends. Not visible to other sessions. No Fail-safe. |
| `LOCAL TEMP` | Alias for TEMPORARY with local scope qualifier. |
| `GLOBAL TEMPORARY` | Temporary table with global scope qualifier (same behaviour in Snowflake as TEMPORARY). |
| `TRANSIENT` | Persists across sessions but has no Fail-safe period (only 0–1 day Time Travel). Reduces storage costs. |

### IF NOT EXISTS

Silently succeeds if the table already exists. Mutually exclusive with `OR REPLACE`.

### Column-level parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `<col_name>` | Identifier | Column name; must follow Snowflake identifier rules. |
| `<col_type>` | Any Snowflake data type | e.g. NUMBER, VARCHAR, TIMESTAMP_NTZ, VARIANT, ARRAY, OBJECT, BOOLEAN. |
| `NOT NULL` | — | Rejects NULL values for the column. |
| `COLLATE` | Collation string | Sets locale-aware string comparison for the column. |
| `DEFAULT <expr>` | Constant, expression, or sequence reference | Value inserted when no explicit value is provided. Cannot be combined with AUTOINCREMENT. |
| `AUTOINCREMENT` / `IDENTITY` | `(seed, step)`, `ORDER` / `NOORDER` | Auto-generates sequential integers. Default seed = 1, step = 1. Only applicable to numeric types. ORDER guarantees monotonically increasing values (slower); NOORDER (default) is faster. |
| `MASKING POLICY` | Policy name | Column-level data masking. Requires APPLY MASKING POLICY privilege. Optional `USING` clause passes additional columns for conditional masking. |
| `PROJECTION POLICY` | Policy name | Controls whether the column can be projected in query results. |
| `TAG` | `tag_name = 'value'` | Attaches one or more object tags to the column. |
| `COMMENT` | String literal | Inline column comment. |

### Table-level parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `CLUSTER BY ( <expr> )` | Column names or expressions | Defines the clustering key for Automatic Clustering. Best for multi-terabyte tables with repetitive filter/join patterns. Avoid on small tables. |
| `ENABLE_SCHEMA_EVOLUTION` | `TRUE` / `FALSE` | When TRUE, new columns encountered during COPY INTO are automatically added to the table schema. Default: FALSE. |
| `DATA_RETENTION_TIME_IN_DAYS` | 0–1 (Standard); 0–90 (Enterprise) | Time Travel window. Set to 0 to disable Time Travel. |
| `MAX_DATA_EXTENSION_TIME_IN_DAYS` | 0–90 | Maximum number of days Snowflake can extend data retention to prevent stream staleness. Default: 14. |
| `CHANGE_TRACKING` | `TRUE` / `FALSE` | Stores hidden metadata columns to track row-level changes. Required for creating streams on the table. Default: FALSE. |
| `DEFAULT_DDL_COLLATION` | Collation string | Sets the default collation for all string columns in the table unless overridden at the column level. |
| `COPY GRANTS` | — | When used with `OR REPLACE`, copies all privileges (except OWNERSHIP) from the old table to the new one. |
| `COPY TAGS` | — | When used with `OR REPLACE`, copies all tags from the old table to the new one. |
| `COMMENT` | String literal | Table-level comment visible in SHOW TABLES and the information schema. |
| `ROW ACCESS POLICY` | Policy name + column list | Row-level security filter applied on every query. Requires APPLY ROW ACCESS POLICY privilege. |
| `AGGREGATION POLICY` | Policy name | Enforces aggregation before returning results. Optional `ENTITY KEY` specifies the entity columns. |
| `JOIN POLICY` | Policy name | Restricts which columns may be used in join conditions. Optional `ALLOWED JOIN KEYS` clause. |
| `STORAGE LIFECYCLE POLICY` | Policy name + column list | Manages data lifecycle (e.g. archiving) based on column values. |
| `TAG` (table-level) | `tag_name = 'value'` | Attaches one or more object tags to the table. |
| `WITH CONTACT` | `purpose = contact_name` | Associates the table with named contacts for a given purpose. |
| `ROW_TIMESTAMP` | `TRUE` / `FALSE` | Enables row-level timestamp tracking metadata. Default: FALSE. |

---

## Access Control Requirements

| Privilege | Object | Notes |
|-----------|--------|-------|
| CREATE TABLE | Schema | Temporary tables are exempt. |
| SELECT | Source table/view | Required for CLONE and CTAS variants. |
| APPLY | Policy / Tag objects | Required when attaching governance policies or tags. |
| OWNERSHIP | Existing table | Required to alter an existing table via CREATE OR ALTER. |

---

## Key Constraints

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Tables and views cannot share the same name within a schema.
- ANSI reserved keywords cannot be used as column names without quoting.
- DDL statements inside a transaction automatically commit the prior open transaction.
- TRANSIENT tables have no Fail-safe period (only 0–1 day Time Travel regardless of edition).
