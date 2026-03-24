---
name: snowflake-create-resource-monitor
description: Consult Snowflake CREATE RESOURCE MONITOR parameter reference before generating any CREATE RESOURCE MONITOR DDL.
---

Before writing a CREATE RESOURCE MONITOR statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE RESOURCE MONITOR IF NOT EXISTS`.
5. Always set CREDIT_QUOTA to a concrete number reflecting the intended budget. Always include at least one NOTIFY trigger (e.g., ON 75 PERCENT DO NOTIFY) before any SUSPEND trigger so administrators receive advance warning. Use SUSPEND (not SUSPEND_IMMEDIATE) as the default action unless immediate cancellation of running queries is explicitly required. Always set FREQUENCY and START_TIMESTAMP together — they are interdependent. List only users in NOTIFY_USERS who have verified email addresses, and observe the 5 non-administrator user maximum.
