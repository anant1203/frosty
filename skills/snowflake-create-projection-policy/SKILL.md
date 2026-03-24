---
name: snowflake-create-projection-policy
description: Consult Snowflake CREATE PROJECTION POLICY parameter reference before generating any CREATE PROJECTION POLICY DDL.
---

Before writing a CREATE PROJECTION POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE PROJECTION POLICY IF NOT EXISTS`.
5. The policy body must call `PROJECTION_CONSTRAINT(ALLOW => {TRUE|FALSE} [, ENFORCEMENT => {'FAIL'|'NULLIFY'}])`.
6. `ALLOW => TRUE` permits column projection (pass-through); `ALLOW => FALSE` restricts it — use the `ENFORCEMENT` argument to control whether restricted queries fail or return NULLs.
7. The default `ENFORCEMENT` is `FAIL`; only specify `NULLIFY` if the user explicitly wants columns silently nullified rather than causing query failures.
8. Projection policies only affect columns in the final result set (outermost SELECT); columns used only in WHERE or JOIN clauses are not blocked. Requires Enterprise Edition or higher.
