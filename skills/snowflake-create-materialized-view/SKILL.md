---
name: snowflake-create-materialized-view
description: Consult Snowflake CREATE MATERIALIZED VIEW parameter reference before generating any CREATE MATERIALIZED VIEW DDL.
---

Before writing a CREATE MATERIALIZED VIEW statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE MATERIALIZED VIEW IF NOT EXISTS`.
5. Materialized views require Snowflake Enterprise Edition or higher; flag this requirement to the user if the edition is unknown.
6. The SELECT statement used to define the materialized view must NOT include HAVING, ORDER BY clauses, or references to stream objects.
7. Add CLUSTER BY only for large datasets where the clustering key matches the most common filter patterns — always include an explicit column list when using CLUSTER BY.
8. Use SECURE only when the user needs to hide the view definition from non-privileged users.
9. Use INTERACTIVE only when the materialized view is based on a single interactive table and low-latency query performance is required.
10. Apply MASKING POLICY, ROW ACCESS POLICY, AGGREGATION POLICY, or TAG clauses only when the user explicitly requests governance controls.
