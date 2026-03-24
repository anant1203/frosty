# CREATE TASK — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-task

## Full Syntax

```sql
CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
  [ WITH TAG ( <tag_name> = '<tag_value>' [, ...] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [, ...] ) ]
  [ { WAREHOUSE = <string> } | { USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string> } ]
  [ SCHEDULE = { '<num> {HOURS | MINUTES | SECONDS}' | 'USING CRON <expr> <time_zone>' } ]
  [ CONFIG = <configuration_string> ]
  [ OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP } ]
  [ <session_parameter> = <value> [, ...] ]
  [ USER_TASK_TIMEOUT_MS = <num> ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
  [ ERROR_INTEGRATION = <integration_name> ]
  [ SUCCESS_INTEGRATION = <integration_name> ]
  [ LOG_LEVEL = '<log_level>' ]
  [ COMMENT = '<string_literal>' ]
  [ FINALIZE = <string> ]
  [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
  [ USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS = <num> ]
  [ TARGET_COMPLETION_INTERVAL = '<num> {HOURS | MINUTES | SECONDS}' ]
  [ SERVERLESS_TASK_MIN_STATEMENT_SIZE = '{ XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE }' ]
  [ SERVERLESS_TASK_MAX_STATEMENT_SIZE = '{ XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE }' ]
  [ AFTER <string> [, <string>, ...] ]
  [ EXECUTE AS USER <user_name> ]
  [ WHEN <boolean_expr> ]
AS
  <sql>
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| `WAREHOUSE` | (none — uses serverless compute if omitted) |
| `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE` | `MEDIUM` (serverless initial size) |
| `SCHEDULE` | (none — required for root/standalone tasks) |
| `CONFIG` | (none) |
| `OVERLAP_POLICY` | `NO_OVERLAP` |
| `USER_TASK_TIMEOUT_MS` | `3600000` (1 hour) |
| `SUSPEND_TASK_AFTER_NUM_FAILURES` | `10` |
| `ERROR_INTEGRATION` | (none) |
| `SUCCESS_INTEGRATION` | (none) |
| `LOG_LEVEL` | (inherits account/session setting) |
| `COMMENT` | (none) |
| `FINALIZE` | (none) |
| `TASK_AUTO_RETRY_ATTEMPTS` | `0` |
| `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS` | (none) |
| `TARGET_COMPLETION_INTERVAL` | (none) |
| `SERVERLESS_TASK_MIN_STATEMENT_SIZE` | (none — auto-sized) |
| `SERVERLESS_TASK_MAX_STATEMENT_SIZE` | (none — auto-sized) |
| `AFTER` | (none — standalone task) |
| `EXECUTE AS USER` | (owner of the task) |
| `WHEN` | (none — always executes) |

## Parameter Descriptions

### `<name>` *(required)*
Unique identifier for the task within the schema. Must start with an alphabetic character; use double quotes for identifiers containing special characters.

### `<sql>` *(required)*
The work the task performs. Must be one of:
- A single SQL statement
- A `CALL` to a stored procedure
- A Snowflake Scripting block (supports multiple statements and control flow)

### `WAREHOUSE = <string>`
Name of the virtual warehouse that provides compute. Omit to use serverless (Snowflake-managed) compute. Mutually exclusive with `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`.

### `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = <string>`
Initial warehouse size for serverless execution. Snowflake auto-tunes after the first successful run and ignores this value afterward.
Valid values: `XSMALL`, `SMALL`, `MEDIUM`, `LARGE`, `XLARGE`, `XXLARGE`.
Default: `MEDIUM`.

### `SCHEDULE`
Defines when a standalone or root task runs. Two formats:
- Interval: `'<num> MINUTES'` / `'<num> HOURS'` / `'<num> SECONDS'` (range: 10 seconds to 8 days)
- Cron: `'USING CRON <expr> <time_zone>'` (minute-level granularity; uses standard 5-field cron)

Required for root and standalone tasks. Must be omitted for child tasks (which use `AFTER`).

### `CONFIG = <configuration_string>`
JSON string accessible by all tasks in a graph via `SYSTEM$GET_TASK_GRAPH_CONFIG()`. Set only on the root task; ignored on child tasks.

### `OVERLAP_POLICY`
Controls concurrent execution behavior.
- `NO_OVERLAP` (default): New run is skipped if a previous run is still active.
- `ALLOW_CHILD_OVERLAP`: Child tasks may overlap with sibling runs.
- `ALLOW_ALL_OVERLAP`: No concurrency restriction.

### `USER_TASK_TIMEOUT_MS = <num>`
Maximum wall-clock time (milliseconds) for a single task run.
Range: `0` to `604800000` (7 days). Default: `3600000` (1 hour).
When combined with statement-level timeouts, the lowest non-zero value wins.

### `SUSPEND_TASK_AFTER_NUM_FAILURES = <num>`
Number of consecutive failures before the task is automatically suspended.
`0` disables automatic suspension. Default: `10`.

### `ERROR_INTEGRATION = <integration_name>`
Name of a notification integration to receive error notifications when the task fails.

### `SUCCESS_INTEGRATION = <integration_name>`
Name of a notification integration to receive success notifications when the task completes.

### `LOG_LEVEL = '<log_level>'`
Controls event-table logging verbosity. Valid values (least to most verbose): `OFF`, `FATAL`, `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`.

### `COMMENT = '<string_literal>'`
Free-text description of the task. Displayed in `SHOW TASKS` and the Snowsight UI.

### `FINALIZE = <string>`
Associates this task as the finalizer for a named root task. A finalizer task:
- Runs after all branches of the DAG complete (or after a failure).
- Cannot have its own schedule or child tasks.

### `TASK_AUTO_RETRY_ATTEMPTS = <num>`
Number of automatic retries if the task run fails. Default: `0` (no retries).

### `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS = <num>`
Minimum gap (seconds) between consecutive triggered task runs. Prevents over-triggering for stream-based tasks.

### `TARGET_COMPLETION_INTERVAL = '<num> {HOURS | MINUTES | SECONDS}'`
Desired completion time for serverless triggered tasks. Valid range: 10 seconds to 1 day.

### `SERVERLESS_TASK_MIN_STATEMENT_SIZE` / `SERVERLESS_TASK_MAX_STATEMENT_SIZE`
Bounds the warehouse size Snowflake selects for serverless execution.
Valid values: `XSMALL`, `SMALL`, `MEDIUM`, `LARGE`, `XLARGE`, `XXLARGE`.

### `AFTER <string> [, ...]`
One or more predecessor task names. Establishes this task as a child in a DAG. Tasks listed here must exist in the same schema.

### `EXECUTE AS USER <user_name>`
Overrides the role context used at execution time. Defaults to the task owner.

### `WHEN <boolean_expr>`
Conditional expression evaluated before each run. Commonly used with:
- `SYSTEM$STREAM_HAS_DATA('<stream_name>')` — skip when no new data
- `SYSTEM$GET_PREDECESSOR_RETURN_VALUE('<task_name>')` — inspect predecessor output

If the condition is FALSE, the task is skipped (a nominal charge may apply for the evaluation).

### `TAG ( <tag_name> = '<tag_value>' [, ...] )`
Attaches governance tags. Tag values are strings up to 256 characters.

### `WITH CONTACT ( <purpose> = <contact_name> [, ...] )`
Associates named contacts with the task for operational ownership metadata.
