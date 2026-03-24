---
name: snowflake-create-service
description: Consult Snowflake CREATE SERVICE parameter reference before generating any CREATE SERVICE DDL.
---

Before writing a CREATE SERVICE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE SERVICE IF NOT EXISTS`.
5. Always include `IN COMPUTE POOL` with the appropriate compute pool name.
6. Choose the correct specification variant: use `FROM SPECIFICATION` for inline or stage-referenced YAML specs, or `FROM SPECIFICATION_TEMPLATE` when the user provides template variables via `USING`.
7. Set `AUTO_SUSPEND_SECS` only when the user wants automatic suspension; the minimum effective value is 300 seconds (0 disables it).
8. Set `MAX_INSTANCES` explicitly when horizontal scaling beyond 1 instance is needed.
9. Include `QUERY_WAREHOUSE` only when service containers will run Snowflake queries.
