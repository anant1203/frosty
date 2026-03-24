---
name: snowflake-create-privacy-policy
description: Consult Snowflake CREATE PRIVACY POLICY parameter reference before generating any CREATE PRIVACY POLICY DDL.
---

Before writing a CREATE PRIVACY POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE PRIVACY POLICY IF NOT EXISTS`.
5. The policy body must call either `NO_PRIVACY_POLICY()` (unrestricted access) or `PRIVACY_BUDGET(BUDGET_NAME => '...' [, ...])` (differential privacy budget).
6. When using a `CASE` expression in the body, always include an `ELSE` clause — every role or user must receive either a privacy budget or unrestricted access; omitting ELSE causes a compilation error.
7. Use context functions such as `CURRENT_ROLE()` or `INVOKER_ROLE()` to conditionally apply budgets per role.
8. For cross-account scenarios, namespace `BUDGET_NAME` with `CURRENT_ACCOUNT()` to avoid budget name collisions.
9. Only override `BUDGET_LIMIT`, `MAX_BUDGET_PER_AGGREGATE`, or `BUDGET_WINDOW` when the user specifies non-default privacy constraints. Requires Enterprise Edition or higher.
