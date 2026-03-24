---
name: snowflake-create-aggregation-policy
description: Consult Snowflake CREATE AGGREGATION POLICY parameter reference before generating any CREATE AGGREGATION POLICY DDL.
---

Before writing a CREATE AGGREGATION POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE AGGREGATION POLICY IF NOT EXISTS`.
5. The policy body must call either `NO_AGGREGATION_CONSTRAINT()` (unrestricted access) or `AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => <n>)` (requires aggregation with at least n rows per group).
6. Aggregation policies require Snowflake Enterprise Edition or higher; warn the user if their account edition is unknown.
7. The policy body cannot reference user-defined functions, tables, or views — only the built-in constraint functions are allowed.
