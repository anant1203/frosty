---
name: snowflake-create-task
description: Consult Snowflake CREATE TASK parameter reference before generating any CREATE TASK DDL.
---

Before writing a CREATE TASK statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE TASK IF NOT EXISTS` where supported.
5. Newly created tasks are always suspended; remind the user to run `ALTER TASK <name> RESUME` after creation.
6. Root and standalone tasks require a `SCHEDULE`; child tasks (those with `AFTER`) must not have one.
7. Prefer serverless compute (omit `WAREHOUSE`, set `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`) unless the user explicitly requests a named warehouse.
8. Only one task should consume from any given stream; advise creating separate streams for multiple consumers.
9. `AUTOCOMMIT` must be TRUE for DML statements executed inside a task.
