---
name: snowflake-create-event-table
description: Consult Snowflake CREATE EVENT TABLE parameter reference before generating any CREATE EVENT TABLE DDL.
---

Before writing a CREATE EVENT TABLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE EVENT TABLE IF NOT EXISTS` where supported.
5. Event tables share a namespace with regular tables and views; ensure the chosen name does not conflict with existing objects in the same schema.
6. `CHANGE_TRACKING = FALSE` is the default; enable it only if the user explicitly needs to track changes via streams.
7. Do not add `CLUSTER BY` unless the table is expected to be multi-terabyte or the user specifically requests it; clustering is not recommended for most event tables.
8. `DATA_RETENTION_TIME_IN_DAYS` defaults to 1; increase it only if the user requires a longer Time Travel window (max 90 days on Enterprise edition).
9. Using `OR REPLACE` on an existing event table drops the old table and makes any existing streams on it stale — warn the user about this side effect if they ask about replacing an existing event table.
