---
name: snowflake-create-masking-policy
description: Consult Snowflake CREATE MASKING POLICY parameter reference before generating any CREATE MASKING POLICY DDL.
---

Before writing a CREATE MASKING POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE MASKING POLICY IF NOT EXISTS`.
5. The return data type in `RETURNS` must exactly match the data type of the first argument (`<arg_name_to_mask>`); cross-type transformations are not allowed.
6. The policy body (`<body>`) must be a valid SQL expression — use conditional functions (e.g. `IFF`, `CASE`) along with masking functions (e.g. `SHA2`, `REGEXP_REPLACE`) or return the column value unchanged.
7. Only set `EXEMPT_OTHER_POLICIES = TRUE` if the user explicitly needs this policy to bypass other row access or conditional masking policies — this setting cannot be changed once the policy is attached to a table or view.
8. For conditional masking policies (multiple arguments), the first argument represents the column to mask; additional arguments provide context values but cannot be virtual columns.
