---
name: snowflake-create-cortex-search
description: Consult Snowflake CREATE CORTEX SEARCH SERVICE parameter reference before generating any CREATE CORTEX SEARCH SERVICE DDL.
---

Before writing a CREATE CORTEX SEARCH SERVICE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE CORTEX SEARCH SERVICE IF NOT EXISTS` where supported.
5. Choose between single-index syntax (`ON <search_column>`) and multi-index syntax (`TEXT INDEXES ... VECTOR INDEXES ...`) based on the user's retrieval requirements; use multi-index when both keyword and vector similarity search are needed.
6. Always specify `WAREHOUSE` and `TARGET_LAG`; they are required.
7. Supply a `PRIMARY KEY` whenever the source table has a natural unique key — it enables optimized incremental refresh.
8. Default `REFRESH_MODE` is INCREMENTAL; only override to FULL when the source table lacks change-tracking support.
