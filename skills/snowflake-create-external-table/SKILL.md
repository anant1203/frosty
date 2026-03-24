---
name: snowflake-create-external-table
description: Consult Snowflake CREATE EXTERNAL TABLE parameter reference before generating any CREATE EXTERNAL TABLE DDL.
---

Before writing a CREATE EXTERNAL TABLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE EXTERNAL TABLE IF NOT EXISTS` where supported.
5. Always specify `LOCATION` (referencing an external stage on S3, Azure, or GCS — internal Snowflake stages are not supported) and `FILE_FORMAT`.
6. All data columns must be defined as virtual columns using expressions against the `VALUE` (VARIANT) pseudocolumn, `METADATA$FILENAME`, or `METADATA$FILE_ROW_NUMBER`; do not attempt to define plain physical columns.
7. `AUTO_REFRESH = TRUE` and `REFRESH_ON_CREATE = TRUE` are the defaults; only override them if the user explicitly opts out of automatic refreshes.
8. Use `PARTITION_TYPE = USER_SPECIFIED` only when the user intends to manage partitions manually via `ALTER EXTERNAL TABLE … ADD PARTITION`.
9. External tables do not support Time Travel, clustering keys, or cloning — do not include those parameters.
