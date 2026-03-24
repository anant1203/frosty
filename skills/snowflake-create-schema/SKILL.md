---
name: snowflake-create-schema
description: Consult Snowflake CREATE SCHEMA parameter reference before generating any CREATE SCHEMA DDL.
---

Before writing a CREATE SCHEMA statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE SCHEMA IF NOT EXISTS`.
5. Choose TRANSIENT only when the user explicitly wants to avoid Fail-safe storage costs; note that all tables created inside a TRANSIENT schema are also transient.
6. Add `WITH MANAGED ACCESS` only when the user wants privilege management centralised on the schema owner rather than individual object owners.
7. Set DATA_RETENTION_TIME_IN_DAYS only when the user specifies a non-default window; default is 1 day (0–1 on Standard, 0–90 on Enterprise).
8. Add Iceberg-related parameters (EXTERNAL_VOLUME, CATALOG, ICEBERG_VERSION_DEFAULT, ENABLE_ICEBERG_MERGE_ON_READ, STORAGE_SERIALIZATION_POLICY) only when the user is building an Iceberg-backed schema.
9. Creating a schema automatically sets it as the active schema for the current session.
