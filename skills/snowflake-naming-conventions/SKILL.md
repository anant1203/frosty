---
name: snowflake-naming-conventions
description: Enforces Snowflake object naming conventions before generating any DDL statement.
---

Before writing any DDL, apply the naming rules in `references/rules.md`.

Steps:
1. Identify the object type being created (table, schema, database, view, stage, etc.)
2. Look up the naming rule for that object type in `references/rules.md`
3. Transform any name provided by the user to conform to the rule before placing it in the DDL
4. If the user-provided name already conforms, use it as-is
5. If you changed a name, note the change in your response so the user is aware
