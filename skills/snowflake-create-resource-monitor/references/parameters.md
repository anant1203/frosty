# CREATE RESOURCE MONITOR — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-resource-monitor

## Full Syntax

```sql
CREATE [ OR REPLACE ] RESOURCE MONITOR [ IF NOT EXISTS ] <name> WITH
  [ CREDIT_QUOTA = <number> ]
  [ FREQUENCY = { MONTHLY | DAILY | WEEKLY | YEARLY | NEVER } ]
  [ START_TIMESTAMP = { <timestamp> | IMMEDIATELY } ]
  [ END_TIMESTAMP = <timestamp> ]
  [ NOTIFY_USERS = ( <user_name> [ , <user_name> , ... ] ) ]
  [ TRIGGERS triggerDefinition [ triggerDefinition ... ] ]
```

### Trigger Definition Sub-syntax

```sql
triggerDefinition ::=
  ON <threshold> PERCENT DO { SUSPEND | SUSPEND_IMMEDIATE | NOTIFY }
```

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the resource monitor within the account. Must start with an alphabetic character. Cannot contain spaces or special characters unless enclosed in double quotes. |

## Optional Parameters Defaults Table

| Parameter | Default |
|-----------|---------|
| `CREDIT_QUOTA` | No quota set (unlimited credits) |
| `FREQUENCY` | Legacy behavior (monthly reset when combined with legacy START_TIMESTAMP) |
| `START_TIMESTAMP` | Legacy behavior (immediate start) |
| `END_TIMESTAMP` | No end date (monitor runs indefinitely) |
| `NOTIFY_USERS` | No users notified |
| `TRIGGERS` | No triggers defined (no automated actions) |

## Optional Parameters — Detailed Descriptions

**`CREDIT_QUOTA = <number>`**
The number of Snowflake credits allocated to this monitor per frequency interval. When cumulative credit usage for the assigned warehouses reaches this number, the monitor is considered at 100% of its quota. Trigger thresholds are expressed as percentages of this value. If not set, the monitor tracks usage but has no quota to trigger against.

**`FREQUENCY = MONTHLY | DAILY | WEEKLY | YEARLY | NEVER`**
Defines how often the credit usage counter resets to zero.
- MONTHLY: Resets on the same calendar day each month (most common for billing-aligned budgets).
- DAILY: Resets every 24 hours from the start timestamp.
- WEEKLY: Resets every 7 days from the start timestamp.
- YEARLY: Resets on the same calendar date each year.
- NEVER: Counter never resets; the quota is a lifetime cap.
FREQUENCY and START_TIMESTAMP are interdependent — if one is specified, the other must also be specified.

**`START_TIMESTAMP = <timestamp> | IMMEDIATELY`**
The date and time when the monitor begins tracking credit usage and the first interval starts. Use IMMEDIATELY to begin at the current timestamp. Format: `YYYY-MM-DD HH:MI [ {+ | -} hh:mi ]`. FREQUENCY and START_TIMESTAMP must be specified together.

**`END_TIMESTAMP = <timestamp>`**
The date and time after which the monitor automatically suspends all assigned warehouses, regardless of credit usage. Useful for project-based or time-bounded budgets. Default: no end date.

**`NOTIFY_USERS = ( <user_name> [ , <user_name> , ... ] )`**
A comma-separated list of Snowflake users who receive email notifications when triggers fire with the NOTIFY action. Constraints:
- Each listed user must have a verified email address in their Snowflake profile.
- A maximum of 5 non-administrator users may be listed (ACCOUNTADMIN users are not subject to this limit).

**`TRIGGERS triggerDefinition [ triggerDefinition ... ]`**
One or more trigger definitions that fire automated actions when cumulative credit usage crosses a threshold.

### Trigger Definition Detail

```
ON <threshold> PERCENT DO { SUSPEND | SUSPEND_IMMEDIATE | NOTIFY }
```

**`<threshold>`**
An integer representing a percentage of CREDIT_QUOTA. Values greater than 100 are supported (useful for overage alerting without suspension at 100%). Each threshold value must be unique within the monitor.

**Actions:**
- **NOTIFY**: Sends an email notification to all users in NOTIFY_USERS and posts an alert in the Snowflake web interface. Does not affect running warehouses.
- **SUSPEND**: Sends a notification and queues a suspend request for all assigned warehouses. Running queries are allowed to complete before warehouses are suspended.
- **SUSPEND_IMMEDIATE**: Sends a notification and immediately suspends all assigned warehouses, cancelling any active queries without allowing them to finish.

**Trigger limits:**
- Maximum 5 NOTIFY-only triggers per resource monitor.
- SUSPEND and SUSPEND_IMMEDIATE triggers count separately; there is no stated limit on them, but best practice is one of each at distinct thresholds.
- Best practice: always place at least one NOTIFY trigger below any SUSPEND threshold so that administrators receive advance warning.

## Behavioral Notes

- After creating a resource monitor, you must assign it to one or more warehouses via `ALTER WAREHOUSE <name> SET RESOURCE_MONITOR = <monitor_name>` or to the entire account via `ALTER ACCOUNT SET RESOURCE_MONITOR = <monitor_name>`.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Only ACCOUNTADMIN can create or modify resource monitors.
- Resource monitors track credits consumed by virtual warehouses, not serverless features (e.g., Snowpipe, automatic clustering).
- The WITH keyword before the parameter list is required syntax.

## Access Control Requirements

Only the ACCOUNTADMIN role can create, modify, or drop resource monitors.
