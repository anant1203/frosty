---
name: snowflake-create-row-access-policy
description: Consult Snowflake CREATE ROW ACCESS POLICY parameter reference before generating any CREATE ROW ACCESS POLICY DDL.
---

Before writing a CREATE ROW ACCESS POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE ROW ACCESS POLICY IF NOT EXISTS`.
5. The policy signature `AS ( <arg_name> <arg_type> [, ...] )` must match the columns it will be attached to; the signature cannot be modified once the policy is attached to a table or view.
6. The body must be a boolean SQL expression; return `TRUE` to expose a row and `FALSE` to hide it.
7. Row access policies are evaluated before masking policies — factor this into the policy logic when both types are applied to the same table.
8. Avoid complex subqueries in the body where possible; subqueries can cause runtime errors in some configurations.
9. The same column cannot appear in both a masking policy signature and a row access policy signature on the same table.
