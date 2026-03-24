---
name: snowflake-create-database
description: Consult Snowflake CREATE DATABASE parameter reference before generating any CREATE DATABASE DDL.
---

Before writing a CREATE DATABASE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE DATABASE IF NOT EXISTS`.
5. If the request implies Iceberg tables, include the relevant Iceberg parameters (EXTERNAL_VOLUME, CATALOG, etc.).
6. If the request implies cloning or replication, use the appropriate syntax variant from the references.
