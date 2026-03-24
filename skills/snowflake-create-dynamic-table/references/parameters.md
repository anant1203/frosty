# CREATE DYNAMIC TABLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table

---

## Full Syntax

```sql
CREATE [ OR REPLACE ] [ TRANSIENT ] DYNAMIC TABLE [ IF NOT EXISTS ] <name> (
    <col_name> <col_type>
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
      [ [ WITH ] PROJECTION POLICY <policy_name> ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
      [ COMMENT '<string_literal>' ]
      [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
    [ , <col_name> <col_type> [ ... ] ]
  )
  TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
  WAREHOUSE = <warehouse_name>
  [ INITIALIZATION_WAREHOUSE = <warehouse_name> ]
  [ REFRESH_MODE = { AUTO | FULL | INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ COMMENT = '<string_literal>' ]
  [ COPY GRANTS ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , <col_name> ... ] ) ] ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ REQUIRE USER ]
  [ IMMUTABLE WHERE ( <expr> ) ]
  [ BACKFILL FROM ]
  [ EXECUTE AS USER <user_name>
    [ USE SECONDARY ROLES { ALL | NONE | <role> [ , ... ] } ]
  ]
  [ ROW_TIMESTAMP = { TRUE | FALSE } ]
  AS <query>
```

---

## Defaults Table

| Parameter | Default | Notes |
|-----------|---------|-------|
| `TRANSIENT` | Permanent (not transient) | Opt-in modifier; omit for permanent tables |
| `TARGET_LAG` | **Required** — no default | Must be `'<num> seconds\|minutes\|hours\|days'` (min 60 s) or `DOWNSTREAM` |
| `WAREHOUSE` | **Required** — no default | Must be a warehouse the role has USAGE on |
| `INITIALIZATION_WAREHOUSE` | Same as `WAREHOUSE` | Used only for initial population / reinitialization |
| `REFRESH_MODE` | `AUTO` | System selects INCREMENTAL if possible, otherwise FULL |
| `INITIALIZE` | `ON_CREATE` | `ON_SCHEDULE` defers initial population to first scheduled refresh |
| `CLUSTER BY` | None | Do not add unless the table will be multi-terabyte |
| `DATA_RETENTION_TIME_IN_DAYS` | `1` (Standard & Enterprise) | Range: 0–90 for permanent, 0–1 for transient |
| `MAX_DATA_EXTENSION_TIME_IN_DAYS` | Inherited from account/schema | Extends retention to prevent stream staleness |
| `COMMENT` | None | Free-text description of the table |
| `COPY GRANTS` | Not set | Retain privileges from replaced table when using OR REPLACE |
| `ROW ACCESS POLICY` | None | Row-level security policy |
| `AGGREGATION POLICY` | None | Aggregation-level security policy |
| `TAG` | None | Metadata tags as name=value pairs |
| `REQUIRE USER` | Not set | Requires a user context for refresh |
| `IMMUTABLE WHERE` | None | Single condition defining immutable data region |
| `EXECUTE AS USER` | Current user | Requires IMPERSONATE privilege on the specified user |
| `USE SECONDARY ROLES` | `NONE` | Secondary roles for the EXECUTE AS USER context |
| `ROW_TIMESTAMP` | `FALSE` | Enables per-row latency measurement |

---

## Parameter Descriptions

### TARGET_LAG *(required)*
Defines the maximum acceptable data freshness lag.

- **Interval form**: `'<num> { seconds | minutes | hours | days }'`
  - Minimum value: 60 seconds.
  - Snowflake will refresh the table at least often enough to keep lag within this bound.
- **DOWNSTREAM**: The table is refreshed only when a downstream dynamic table that depends on it is refreshed. Use this when building pipelines where freshness is governed by the final consumer.

### WAREHOUSE *(required)*
Name of the virtual warehouse that provides compute for scheduled refreshes. The executing role must hold USAGE privilege on this warehouse.

### INITIALIZATION_WAREHOUSE
An optional separate warehouse used only for the initial population (and any reinitialization). Useful to isolate large one-time loads from ongoing refresh compute costs.

### REFRESH_MODE
Controls the algorithm used to refresh the dynamic table.

| Value | Behaviour |
|-------|-----------|
| `AUTO` (default) | Snowflake chooses INCREMENTAL if the query supports it; falls back to FULL otherwise |
| `INCREMENTAL` | Only changed rows are processed. Requires queries that Snowflake can incremental-refresh (no unsupported constructs). |
| `FULL` | The entire result set is recomputed on every refresh cycle. |

### INITIALIZE
Controls when the first refresh population happens.

| Value | Behaviour |
|-------|-----------|
| `ON_CREATE` (default) | The table is populated synchronously during the CREATE statement. |
| `ON_SCHEDULE` | The table starts empty; the first population occurs at the next scheduled refresh time. |

### TRANSIENT
When specified, the table does not maintain a Fail-Safe storage layer (7-day period after Time Travel). Reduces storage costs. `DATA_RETENTION_TIME_IN_DAYS` is capped at 1 for transient tables.

### CLUSTER BY
Defines a list of expressions used as the clustering key. Improves pruning performance for large tables queried with selective predicates on those expressions. Not recommended for tables smaller than a few terabytes.

### DATA_RETENTION_TIME_IN_DAYS
Number of days that historical data is retained for Time Travel (`AT`/`BEFORE` queries). Range: `0–90` for permanent tables; `0–1` for transient tables.

### MAX_DATA_EXTENSION_TIME_IN_DAYS
Maximum number of extra days Snowflake may extend the retention period beyond `DATA_RETENTION_TIME_IN_DAYS` to prevent streams on this table from becoming stale.

### COPY GRANTS
When using `CREATE OR REPLACE`, retains the access privileges from the original table. Cannot appear after the `AS <query>` clause.

### ROW ACCESS POLICY
Applies a row-level security policy. Syntax: `WITH ROW ACCESS POLICY <policy_name> ON (<col_name> [, ...])`.

### AGGREGATION POLICY
Applies an aggregation-level security policy. Optional `ENTITY KEY` specifies the entity granularity columns.

### REQUIRE USER
When set, the dynamic table refresh requires a user context. Used in conjunction with `EXECUTE AS USER`.

### IMMUTABLE WHERE
A single Boolean expression defining the immutable data region. Rows matching the expression cannot be modified by refreshes. Restrictions:
- No subqueries
- No nondeterministic functions (except timestamp functions that do not create a shrinking immutable region)
- No user-defined or external functions
- No metadata columns
- No window function or aggregate results

### EXECUTE AS USER
Runs refreshes under the security context of the specified user. Requires the executing role to hold `IMPERSONATE` privilege on that user. Optionally qualified with `USE SECONDARY ROLES { ALL | NONE | <role> [, ...] }`.

### ROW_TIMESTAMP
When `TRUE`, Snowflake records a hidden timestamp column per row that can be used to measure per-row data latency.

### AS \<query\> *(required)*
The SELECT query that defines the dynamic table's content. This clause must be the last element in the CREATE statement.

---

## Important Usage Notes

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Change tracking must be enabled on all base objects (tables, views) that the dynamic table queries.
- When chaining dynamic tables, downstream table `TARGET_LAG` must be >= upstream table `TARGET_LAG`.
- Cloned dynamic tables start in a **suspended** state.
- `ORDER BY` inside the defining query is not propagated to callers; sort when querying the dynamic table directly.
- `CREATE OR REPLACE` is atomic — the old table is dropped and a new one created in a single transaction.
