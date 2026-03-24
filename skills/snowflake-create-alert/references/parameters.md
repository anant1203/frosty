# CREATE ALERT — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-alert

## Full Syntax

```sql
CREATE [ OR REPLACE ] ALERT [ IF NOT EXISTS ] <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [, <tag_name> = '<tag_value>' , ...] ) ]
  [ SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }' ]
  [ WAREHOUSE = <warehouse_name> ]
  [ COMMENT = '<string_literal>' ]
  IF( EXISTS(
    <condition>
  ))
  THEN
    <action>
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| `SCHEDULE` | (none — streaming alert, triggers on new data) |
| `WAREHOUSE` | (none — uses serverless compute if omitted) |
| `COMMENT` | (none) |
| `TAG` | (none) |
| Alert state at creation | `SUSPENDED` |

## Parameter Descriptions

### `<name>` *(required)*
Unique identifier for the alert within its schema. Must start with an alphabetic character. Use double quotes for identifiers containing spaces or special characters (case-sensitive when quoted).

### `IF( EXISTS( <condition> ) )` *(required)*
The trigger condition. A SQL statement whose result set is inspected:
- If one or more rows are returned, the condition is considered TRUE and the `THEN` action is executed.
- If zero rows are returned, the action is skipped.

Accepted statement types: `SELECT`, `SHOW`, `CALL`.

Example: `SELECT * FROM sensor_readings WHERE temperature > 100`

### `THEN <action>` *(required)*
The SQL statement executed when the condition returns rows. Common patterns:
- `CALL SYSTEM$SEND_EMAIL(...)` — send an email notification
- `CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(...)` — send a Snowflake notification
- Any valid SQL DML or stored procedure call

### `SCHEDULE`
Determines how frequently the alert evaluates its condition.

Two formats:
- **Interval:** `'<num> MINUTE'` — evaluates every `<num>` minutes. Maximum: `11520` minutes (8 days).
- **Cron:** `'USING CRON <expr> <time_zone>'` — evaluates on a cron schedule.

**Cron expression format (5 fields):**
```
<minute> <hour> <day-of-month> <month> <day-of-week>
```
Field ranges:
- `minute`: 0–59
- `hour`: 0–23
- `day-of-month`: 1–31 (supports `L` for last day)
- `month`: 1–12
- `day-of-week`: 0–6 (0 = Sunday; supports `L` for last occurrence)

Special characters: `*` (wildcard), `/<n>` (every nth), `L` (last).

**Omitting SCHEDULE (or setting to NULL):** Creates a streaming-style alert that triggers automatically when new data arrives, without a fixed polling interval.

### `WAREHOUSE = <warehouse_name>`
Named virtual warehouse used to execute the condition and action queries. If omitted, Snowflake uses serverless (Snowflake-managed) compute.

### `COMMENT = '<string_literal>'`
Free-text description of the alert. Visible in `SHOW ALERTS` output and the Snowsight UI.

### `TAG ( <tag_name> = '<tag_value>' [, ...] )`
Attaches governance tags to the alert. Tag values are strings up to 256 characters.

## Key Behavioral Notes

- Newly created alerts are **suspended by default**. Run `ALTER ALERT <name> RESUME` to activate the alert after creation.
- Alerts execute using the **owner role's** privileges. The owner must have access to all objects referenced in the condition and action.
- Limited validation occurs at creation time; errors in the condition or action SQL surface only at execution time.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive; never use both in the same statement.
- To pause an active alert: `ALTER ALERT <name> SUSPEND`.
- To view recent execution history: query `SNOWFLAKE.ACCOUNT_USAGE.ALERT_HISTORY`.
