---
name: snowflake-create-role
description: Consult Snowflake CREATE ROLE parameter reference before generating any CREATE ROLE DDL.
---

Before writing a CREATE ROLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE ROLE IF NOT EXISTS`.
5. Always add a COMMENT that describes the role's purpose and intended privilege scope. After creating a role, remind the user that the role must be explicitly granted to users or other roles before it is usable, and that the role itself must also be granted the USAGE privilege on any objects it needs to access.
