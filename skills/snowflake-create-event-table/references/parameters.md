# CREATE EVENT TABLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-event-table

---

## Full Syntax

### Standard form

```sql
CREATE [ OR REPLACE ] EVENT TABLE [ IF NOT EXISTS ] <name>
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ COPY GRANTS ]
  [ [ WITH ] COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
```

### Clone variant

```sql
CREATE [ OR REPLACE ] EVENT TABLE [ IF NOT EXISTS ] <name>
  CLONE <source_table>
    [ { AT | BEFORE } (
        { TIMESTAMP => <timestamp>
        | OFFSET    => <time_difference>
        | STATEMENT => <id>
        }
      )
    ]
    [ COPY GRANTS ]
    [ CLUSTER BY ( <expr> [ , ... ] ) ]
    [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
    [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
    [ CHANGE_TRACKING = { TRUE | FALSE } ]
    [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
    [ COMMENT = '<string_literal>' ]
    [ ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] ) ]
    [ TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

---

## Defaults Table

| Parameter | Default | Notes |
|-----------|---------|-------|
| `CLUSTER BY` | None | Not recommended unless the table is multi-terabyte |
| `DATA_RETENTION_TIME_IN_DAYS` | `1` (Standard & Enterprise) | Range: 0–90 (Enterprise); 0–1 (Standard) |
| `MAX_DATA_EXTENSION_TIME_IN_DAYS` | Inherited from account/schema | Extends retention to prevent stream staleness |
| `CHANGE_TRACKING` | `FALSE` | Set `TRUE` to enable streams on this event table |
| `DEFAULT_DDL_COLLATION` | None (account default) | Collation specification for columns in the table |
| `COPY GRANTS` | Not set | Retain privileges from replaced/cloned table |
| `COMMENT` | None | Free-text description of the table |
| `ROW ACCESS POLICY` | None | Row-level security policy |
| `TAG` | None | Metadata tags as name=value pairs (max 256 chars each) |
| `WITH CONTACT` | None | Associates contacts with defined purposes |

---

## Parameter Descriptions

### name *(required)*
Unique identifier for the event table within the schema. Must begin with an alphabetic character. A schema cannot contain event tables, regular tables, and views with the same name — all three share the same namespace.

### CLUSTER BY
Defines one or more expressions as the clustering key. Improves pruning on large tables queried with selective predicates on the clustering expressions.

**Not recommended for most event tables** — only add for tables expected to reach multi-terabyte size. Adding an inappropriate clustering key wastes compute on automatic reclustering.

### DATA_RETENTION_TIME_IN_DAYS
Specifies how many days of historical data are retained for Time Travel (AT/BEFORE queries and UNDROP).

- Standard edition: `0` or `1` (default `1`)
- Enterprise edition: `0–90` (default `1`)

Set to `0` to disable Time Travel entirely (reduces storage cost; no recovery possible via Time Travel).

### MAX_DATA_EXTENSION_TIME_IN_DAYS
The maximum number of additional days beyond `DATA_RETENTION_TIME_IN_DAYS` that Snowflake may extend retention to keep streams on this table from becoming stale. If no streams exist, this parameter has no effect.

### CHANGE_TRACKING
When `TRUE`, Snowflake adds hidden metadata columns to the table that track row-level changes. These columns are consumed by streams created on this event table. Default: `FALSE`.

### DEFAULT_DDL_COLLATION
Sets the default collation specification for string columns created in this table. Follows the standard Snowflake collation specification syntax (e.g., `'en-ci'` for case-insensitive English). An empty string (`''`) disables any database-level default.

### COPY GRANTS
When using `CREATE OR REPLACE` or `CLONE`, retains all access privileges (except OWNERSHIP) from the original event table. Without this option, the new table has no privileges other than those granted to the creator's role.

### COMMENT
A free-text string that documents the event table. Can be included with or without the `WITH` keyword.

### ROW ACCESS POLICY
Applies a row-level security policy to the event table. Syntax:

```sql
[ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] )
```

Columns listed must exist in the event table (note: event tables have a fixed schema with pre-defined columns such as `TIMESTAMP`, `RESOURCE_ATTRIBUTES`, `RECORD`, etc.).

### TAG
Assigns object-level metadata tags. Format:

```sql
[ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] )
```

Tag values must be 256 characters or fewer.

### WITH CONTACT
Associates named contacts with specific purposes for this event table. Used for governance and notification workflows.

### CLONE \<source_table\>
Creates an event table as a zero-copy clone of the source event table. Optionally scope the clone to a point in time using `AT` or `BEFORE` with `TIMESTAMP`, `OFFSET`, or `STATEMENT` qualifiers.

---

## Important Usage Notes

- **Namespace collision**: A schema cannot contain an event table, a regular table, and a view with the same name. All three share one namespace.
- **OR REPLACE behaviour**: Equivalent to `DROP EVENT TABLE` on the existing table followed by `CREATE`. The dropped table enters Fail-Safe (it is not permanently deleted immediately), but any streams on the old table become **stale and unreadable**.
- **Atomic operations**: `CREATE OR REPLACE` is atomic — concurrent queries see either the old or the new table version, never a partial state.
- **OR REPLACE and IF NOT EXISTS are mutually exclusive.**
- **Clustering keys**: Not intended for all tables. Only add `CLUSTER BY` for very large (multi-terabyte) event tables where query patterns will benefit from pruning on the clustering expressions.
- Event tables have a **fixed predefined schema** (e.g., `TIMESTAMP`, `START_TIMESTAMP`, `OBSERVED_TIMESTAMP`, `TRACE`, `RESOURCE_ATTRIBUTES`, `RECORD_TYPE`, `RECORD`, `RECORD_ATTRIBUTES`). Column definitions are not specified in the CREATE statement.
