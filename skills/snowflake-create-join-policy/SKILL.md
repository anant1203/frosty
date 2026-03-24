---
name: snowflake-create-join-policy
description: Consult Snowflake CREATE JOIN POLICY parameter reference before generating any CREATE JOIN POLICY DDL.
---

Before writing a CREATE JOIN POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE JOIN POLICY IF NOT EXISTS`.
5. The policy body must call `JOIN_CONSTRAINT(JOIN_REQUIRED => <boolean_expression>)`. Use `TRUE` to enforce that queries must join to another table; use `FALSE` to allow unrestricted queries (equivalent to no policy).
6. The allowed join columns are configured when the policy is assigned to a table or view (`ALTER TABLE ... SET JOIN POLICY`), not in the CREATE statement itself.
7. The policy body cannot reference user-defined functions, tables, or views.
