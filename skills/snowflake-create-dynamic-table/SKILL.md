---
name: snowflake-create-dynamic-table
description: Consult Snowflake CREATE DYNAMIC TABLE parameter reference before generating any CREATE DYNAMIC TABLE DDL.
---

Before writing a CREATE DYNAMIC TABLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE DYNAMIC TABLE IF NOT EXISTS` where supported.
5. Always specify both `TARGET_LAG` and `WAREHOUSE` — they are required. Choose `TARGET_LAG = DOWNSTREAM` only when the dynamic table feeds other dynamic tables and downstream refresh semantics are desired; otherwise use an explicit interval (e.g., `'1 minutes'`).
6. Prefer `REFRESH_MODE = AUTO` unless the user explicitly requires `FULL` or `INCREMENTAL`; the system will choose the most efficient mode automatically.
7. Do not add `CLUSTER BY` unless the table is expected to be multi-terabyte or the user requests it.
8. Do not use `EXECUTE AS USER` unless the user explicitly provides an impersonation user, as it requires the IMPERSONATE privilege.
9. Append the defining query as the `AS <query>` clause at the end of the statement — it is required.
