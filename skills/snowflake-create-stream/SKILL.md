---
name: snowflake-create-stream
description: Consult Snowflake CREATE STREAM parameter reference before generating any CREATE STREAM DDL.
---

Before writing a CREATE STREAM statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE STREAM IF NOT EXISTS` where supported.
5. Choose the correct syntax variant based on the target object type: TABLE, EXTERNAL TABLE, STAGE (directory table), DYNAMIC TABLE, or VIEW.
6. For insert-heavy workloads on standard tables or views, recommend `APPEND_ONLY = TRUE` to improve performance.
7. For external tables, `INSERT_ONLY = TRUE` is required.
8. Streams on geospatial columns should use `APPEND_ONLY = TRUE` as standard streams cannot retrieve geospatial change data.
9. `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive; never combine them.
