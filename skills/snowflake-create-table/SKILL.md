---
name: snowflake-create-table
description: Consult Snowflake CREATE TABLE parameter reference before generating any CREATE TABLE DDL.
---

Before writing a CREATE TABLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE TABLE IF NOT EXISTS`.
5. Choose the correct table type: permanent (default), TRANSIENT (no Fail-safe, lower cost), or TEMPORARY/TEMP/VOLATILE (session-scoped, dropped at session end). Default to permanent unless the user implies otherwise.
6. For CTAS (CREATE TABLE … AS SELECT), omit column definitions when the SELECT list already provides unambiguous names and types.
7. Use CLUSTER BY only for very large (multi-terabyte) tables where the chosen clustering key matches common filter/join patterns — do not add it speculatively.
8. Enable CHANGE_TRACKING = TRUE only when the user explicitly needs CDC or stream support on the table.
9. Set DATA_RETENTION_TIME_IN_DAYS only when the user specifies a non-default retention window; the platform default is 1 day.
10. Apply MASKING POLICY, ROW ACCESS POLICY, AGGREGATION POLICY, or TAG clauses only when the user explicitly requests governance controls.
