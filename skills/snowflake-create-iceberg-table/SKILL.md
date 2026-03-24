---
name: snowflake-create-iceberg-table
description: Consult Snowflake CREATE ICEBERG TABLE parameter reference before generating any CREATE ICEBERG TABLE DDL.
---

Before writing a CREATE ICEBERG TABLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE ICEBERG TABLE IF NOT EXISTS` where supported.
5. Always specify `EXTERNAL_VOLUME` and `BASE_LOCATION` when Snowflake is the catalog (the most common case); omit them only when integrating an external catalog.
6. `CATALOG = 'SNOWFLAKE'` is the default; omit it unless you are referencing an external catalog integration.
7. `STORAGE_SERIALIZATION_POLICY = COMPATIBLE` is the default; use `OPTIMIZED` only when the user explicitly wants Snowflake-optimised encoding and compression and does not need to read the files with other engines.
8. Note that `NOT NULL` and `UNIQUE` constraints on `PRIMARY KEY` columns are represented in Iceberg metadata as identifier fields but are **not enforced** by Snowflake at DML time.
9. Do not add `CLUSTER BY` unless the table is expected to be very large or the user requests it.
10. Use `PARTITION BY` only when the user specifies a partitioning strategy; choose identity, bucket, truncate, or temporal transforms as appropriate.
