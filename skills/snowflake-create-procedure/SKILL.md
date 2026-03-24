---
name: snowflake-create-procedure
description: Consult Snowflake CREATE PROCEDURE parameter reference before generating any CREATE PROCEDURE DDL.
---

Before writing a CREATE PROCEDURE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE PROCEDURE IF NOT EXISTS` where supported.
5. Confirm the handler language (SQL/Snowflake Scripting, JavaScript, Python, Java, or Scala) before generating code; each language has distinct required parameters (`RUNTIME_VERSION`, `PACKAGES`, `HANDLER`).
6. Default execution context is `EXECUTE AS OWNER`; switch to `EXECUTE AS CALLER` only when the procedure must run with the caller's privileges.
7. Stored procedures support overloading by argument count or data types; ensure the signature is unambiguous.
8. Procedures are not atomic — individual statement failures do not automatically roll back the entire procedure; advise explicit transaction control when needed.
