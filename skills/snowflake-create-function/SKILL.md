---
name: snowflake-create-function
description: Consult Snowflake CREATE FUNCTION parameter reference before generating any CREATE FUNCTION DDL.
---

Before writing a CREATE FUNCTION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE FUNCTION IF NOT EXISTS` where supported.
5. Select the correct LANGUAGE clause (SQL, JAVASCRIPT, PYTHON, JAVA, SCALA) based on the user's intent; when the language is ambiguous, prefer SQL for simple transformations and Python for complex logic.
6. For tabular UDFs use `RETURNS TABLE (col_name col_data_type [, ...])` instead of a scalar return type.
7. Python UDFs require an explicit `RUNTIME_VERSION`; Java and Scala UDFs require a `HANDLER` pointing to the class/method.
8. Place optional arguments (those with DEFAULT values) after all required arguments in the signature.
9. Use `RETURNS NULL ON NULL INPUT` (STRICT) when the function has no meaningful behavior on NULLs, to avoid unnecessary invocations.
