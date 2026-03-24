---
name: snowflake-create-session-policy
description: Consult Snowflake CREATE SESSION POLICY parameter reference before generating any CREATE SESSION POLICY DDL.
---

Before writing a CREATE SESSION POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE SESSION POLICY IF NOT EXISTS`.
5. SESSION_IDLE_TIMEOUT_MINS applies to all Snowflake clients and programmatic connections; SESSION_UI_IDLE_TIMEOUT_MINS applies only to Snowsight. Set both when the user needs consistent behavior across interfaces.
6. BLOCKED_SECONDARY_ROLES takes precedence over ALLOWED_SECONDARY_ROLES; avoid specifying the same role in both lists.
7. Remind the user that the policy must be attached to a user or account with `ALTER USER SET SESSION_POLICY` or `ALTER ACCOUNT SET SESSION_POLICY` to take effect.
