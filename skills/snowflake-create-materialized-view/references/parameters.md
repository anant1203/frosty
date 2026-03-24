# Snowflake CREATE MATERIALIZED VIEW — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-materialized-view

---

## Full Syntax

```sql
CREATE [ OR REPLACE ] [ SECURE ] [ INTERACTIVE ] MATERIALIZED VIEW [ IF NOT EXISTS ] <name>
  [ COPY GRANTS ]
  ( <column_list> )
  [ <col1> [ WITH ] MASKING POLICY <policy_name> [ USING ( <col1>, <cond_col1>, ... ) ]
            [ WITH ] PROJECTION POLICY <policy_name>
            [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>', ... ] ) ]
  [ , <col2> [ ... ] ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , <col_name> ... ] ) ] ]
  [ CLUSTER BY ( <expr1> [ , <expr2> ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>', ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
  AS <select_statement>
```

---

## Defaults Table

| Parameter | Default |
|-----------|---------|
| SECURE | Not secure |
| INTERACTIVE | Standard materialized view |
| IF NOT EXISTS | Not set (error if MV exists) |
| COPY GRANTS | Not applied |
| column_list | None (required when CLUSTER BY is used) |
| MASKING POLICY (column) | None |
| PROJECTION POLICY (column) | None |
| COMMENT | None |
| ROW ACCESS POLICY | None |
| AGGREGATION POLICY | None |
| CLUSTER BY | None |
| TAG | None |
| WITH CONTACT | None |

---

## Parameter Descriptions

### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the materialized view within the schema. Must begin with an alphabetic character. Special characters require double-quoting. |
| `<select_statement>` | SQL query that defines the materialized view's result set. Must NOT include `HAVING`, `ORDER BY` clauses, or references to stream objects. The results are physically stored and automatically maintained by Snowflake. |

### Creation modifiers

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `OR REPLACE` | — | Atomically replaces an existing materialized view with the same name. Mutually exclusive with `IF NOT EXISTS`. |
| `IF NOT EXISTS` | — | Silently succeeds if the materialized view already exists. Mutually exclusive with `OR REPLACE`. |
| `SECURE` | — | Hides the view definition and execution plan from users who do not own the materialized view (similar to secure regular views). Use when the underlying query logic or column structure must not be exposed. |
| `INTERACTIVE` | — | Creates an interactive materialized view optimized for low-latency queries. Must be based on a single interactive table. Provides faster query response at the cost of additional resource usage. |
| `COPY GRANTS` | — | When used with `OR REPLACE`, copies all privileges (except OWNERSHIP) from the replaced materialized view to the new one. |

### Column-level parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `<column_list>` | Comma-separated column names | Explicit column names for the materialized view. Required when `CLUSTER BY` is specified. Data types are not required in the column list. |
| `MASKING POLICY` | Policy name | Applies data masking to a column. The optional `USING` clause provides additional columns for conditional masking (first argument must be the masked column). |
| `PROJECTION POLICY` | Policy name | Restricts whether the column can appear in query result projections. |
| `TAG` (column-level) | `tag_name = 'value'` | Attaches object tags to individual columns. Values are strings up to 256 characters. |

### View-level parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `COMMENT` | String literal | Description of the materialized view, visible in SHOW MATERIALIZED VIEWS and the information schema. |
| `ROW ACCESS POLICY` | Policy name + column list | Applies a row-level security filter to every query on the materialized view. |
| `AGGREGATION POLICY` | Policy name | Enforces aggregation of results before returning them. Optional `ENTITY KEY` specifies the entity-level grouping columns. |
| `CLUSTER BY ( <expr> )` | Column names or expressions | Defines the clustering key for the materialized view's stored data. Recommended for large result sets with repetitive filter patterns. Requires an explicit `<column_list>` when used. |
| `TAG` (view-level) | `tag_name = 'value'` | Attaches object tags to the materialized view. |
| `WITH CONTACT` | `purpose = contact_name` | Associates the materialized view with named contacts for a given purpose. |

---

## SELECT Statement Restrictions

The following constructs are **not allowed** in the defining SELECT statement of a materialized view:

- `HAVING` clause
- `ORDER BY` clause
- References to stream objects
- Non-deterministic functions (e.g. `CURRENT_TIMESTAMP`, `RANDOM()`, `SEQ`)
- UDFs (user-defined functions) in certain contexts
- Subqueries in the WHERE clause that reference the same base table
- `LIMIT` / `FETCH` clauses

---

## Key Constraints

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Materialized views require **Snowflake Enterprise Edition** or higher.
- A materialized view cannot share a name with a table or regular view in the same schema.
- `CLUSTER BY` requires an explicit `<column_list>` to be specified.
- `INTERACTIVE` materialized views must be based on a single interactive table.
- Snowflake automatically maintains (refreshes) the materialized view as the base table changes; manual refresh is not required.

---

## Access Control Requirements

| Privilege | Object |
|-----------|--------|
| CREATE MATERIALIZED VIEW | Schema |
| SELECT | Base table(s) referenced in the SELECT statement |
| APPLY | Policy / Tag objects (when attaching governance policies or tags) |
