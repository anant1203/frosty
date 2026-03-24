---
name: snowflake-create-alert
description: Consult Snowflake CREATE ALERT parameter reference before generating any CREATE ALERT DDL.
---

Before writing a CREATE ALERT statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE ALERT IF NOT EXISTS` where supported.
5. Newly created alerts are suspended by default; remind the user to run `ALTER ALERT <name> RESUME` after creation.
6. The `IF( EXISTS( <condition> ))` block accepts SELECT, SHOW, or CALL statements; the action fires whenever one or more rows are returned.
7. For the `THEN <action>` block, use `SYSTEM$SEND_EMAIL` or `SYSTEM$SEND_SNOWFLAKE_NOTIFICATION` for notification-based alerts.
8. Omit `SCHEDULE` (or set to NULL) to create a streaming alert that triggers on new data; otherwise supply a cron expression or minute interval.
9. `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive; never combine them.
