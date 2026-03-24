---
name: snowflake-create-semantic-view
description: Consult Snowflake CREATE SEMANTIC VIEW parameter reference before generating any CREATE SEMANTIC VIEW DDL.
---

Before writing a CREATE SEMANTIC VIEW statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE SEMANTIC VIEW IF NOT EXISTS` where supported.
5. Every semantic view must include a `TABLES` clause; at least one `DIMENSIONS` or `METRICS` clause is also required for the view to be valid.
6. Define `RELATIONSHIPS` whenever two or more logical tables must be joined; specify join type (standard, ASOF, or range) explicitly.
7. Populate `AI_SQL_GENERATION` with concise natural-language instructions that guide Cortex Analyst when generating SQL from the view.
8. Mark fact expressions `PRIVATE` when they should not be exposed directly to end users; dimensions are always `PUBLIC`.
