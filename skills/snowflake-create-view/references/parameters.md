# Snowflake CREATE VIEW — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-view

---

## Full Syntax

### Standard CREATE VIEW

```sql
CREATE [ OR REPLACE ] [ SECURE ] [ { [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE } ]
  [ RECURSIVE ] VIEW [ IF NOT EXISTS ] <name>
  [ ( <column_list> ) ]
  [ <col1> [ WITH ] MASKING POLICY <policy_name> [ USING ( <col1>, <cond_col1>, ... ) ]
            [ WITH ] PROJECTION POLICY <policy_name>
            [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ , <col2> [ ... ] ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , ... ] ) ] ]
  [ [ WITH ] JOIN POLICY <policy_name> [ ALLOWED JOIN KEYS ( <col_name> [ , ... ] ) ] ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , ... ] ) ]
  AS <select_statement>
```

### CREATE OR ALTER VIEW (Preview Feature)

```sql
CREATE OR ALTER [ SECURE ] [ { [ { LOCAL | GLOBAL } ] TEMP | TEMPORARY | VOLATILE } ]
  [ RECURSIVE ] VIEW <name>
  [ ( <column_list> ) ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  AS <select_statement>
```

Creates the view if it does not exist, or replaces its definition while preserving grants and other properties.

---

## Defaults Table

| Parameter | Default |
|-----------|---------|
| SECURE | Not secure (definition visible to authorized users) |
| TEMP / TEMPORARY / VOLATILE | Permanent view |
| RECURSIVE | Non-recursive |
| IF NOT EXISTS | Not set (error if view exists) |
| CHANGE_TRACKING | FALSE |
| COPY GRANTS | Not applied |
| COMMENT | None |
| MASKING POLICY (column) | None |
| PROJECTION POLICY (column) | None |
| ROW ACCESS POLICY | None |
| AGGREGATION POLICY | None |
| JOIN POLICY | None |
| TAG | None |

---

## Parameter Descriptions

### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the view within the schema. Must begin with an alphabetic character. Special characters are allowed if enclosed in double quotes. Cannot share a name with an existing table in the same schema. |
| `<select_statement>` | SQL query that defines the view's result set. Based on one or more tables, other views, or valid SELECT expressions. Maximum size: 95 KB. |

### Creation modifiers

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `OR REPLACE` | — | Atomically replaces an existing view with the same name. Mutually exclusive with `IF NOT EXISTS`. |
| `IF NOT EXISTS` | — | Silently succeeds if the view already exists. Mutually exclusive with `OR REPLACE`. |
| `SECURE` | — | Designates the view as a secure view. The view definition and query execution details are hidden from users who do not own the view (e.g. hidden from EXPLAIN output). Use when business logic or sensitive column structure must not be exposed. |
| `RECURSIVE` | — | Allows the SELECT statement to reference the view itself (self-referencing / hierarchical queries). An explicit column list is required when RECURSIVE is specified. |

### Temporary view modifiers (mutually exclusive with each other)

| Keyword | Description |
|---------|-------------|
| `TEMPORARY` / `TEMP` | Session-scoped view — automatically dropped when the session ends. Not visible to other sessions. |
| `VOLATILE` | Alias for TEMPORARY in Snowflake. |
| `LOCAL TEMP` | TEMPORARY with local scope qualifier. |
| `GLOBAL TEMPORARY` | TEMPORARY with global scope qualifier (same runtime behaviour in Snowflake). |

### Column-level parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `<column_list>` | Comma-separated column names | Explicit column names for the view. Required when RECURSIVE is used; required when the SELECT list contains unnamed expression columns. |
| `MASKING POLICY` | Policy name | Applies data masking to a column in the view. The optional `USING` clause provides additional columns for conditional masking logic (first argument must be the masked column itself). |
| `PROJECTION POLICY` | Policy name | Restricts whether the column can appear in query result projections based on user context. |
| `TAG` (column-level) | `tag_name = 'value'` | Attaches object tags to individual columns. Tag values are strings up to 256 characters. |

### View-level parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `ROW ACCESS POLICY` | Policy name + column list | Applies a row-level security filter to every query on the view. The ON clause lists the columns passed to the policy function. |
| `CHANGE_TRACKING` | `TRUE` / `FALSE` | Enables hidden metadata columns required for creating a stream on the view, enabling CDC (change data capture) scenarios. Default: FALSE. |
| `COPY GRANTS` | — | When used with `OR REPLACE`, copies all privileges (except OWNERSHIP) from the replaced view to the new view definition. |
| `COMMENT` | String literal (max 256 chars) | View-level description visible in SHOW VIEWS and the information schema. Can also be specified per column. |
| `AGGREGATION POLICY` | Policy name | Enforces that query results must be aggregated before being returned. Optional `ENTITY KEY` specifies the entity-level grouping columns. |
| `JOIN POLICY` | Policy name | Restricts which columns in the view may be used as join keys in queries. Optional `ALLOWED JOIN KEYS` clause lists the permitted columns. |
| `TAG` (view-level) | `tag_name = 'value'` | Attaches object tags to the view itself. |
| `WITH CONTACT` | `purpose = contact_name` | Associates the view with named contacts for a given purpose. |

---

## Key Constraints

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- A table and a view cannot share the same name within a schema.
- The SELECT statement is limited to 95 KB.
- Views can be nested up to 20 levels deep.
- Columns derived from expressions must be given explicit aliases (either in the SELECT list or via `<column_list>`).
- When RECURSIVE is used, an explicit column list is required.
- Secure views hide the view definition and execution plan from non-owners; query performance may be slightly affected.

---

## Access Control Requirements

| Privilege | Object |
|-----------|--------|
| CREATE VIEW | Schema |
| SELECT | All tables and views referenced in the SELECT statement |
| APPLY | Policy / Tag objects (when attaching governance policies or tags) |
