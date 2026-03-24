---
name: snowflake-create-database-role
description: Consult Snowflake CREATE DATABASE ROLE parameter reference before generating any CREATE DATABASE ROLE DDL.
---

Before writing a CREATE DATABASE ROLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE DATABASE ROLE IF NOT EXISTS`.
5. Always qualify the role name with the target database (e.g., `<db_name>.<role_name>`) unless the current session database is already confirmed. Always add a COMMENT describing the role's purpose. Note that upon creation Snowflake automatically grants the USAGE privilege on the containing database to the new database role, so an explicit GRANT for that is not needed.
