---
name: snowflake-create-image-repository
description: Consult Snowflake CREATE IMAGE REPOSITORY parameter reference before generating any CREATE IMAGE REPOSITORY DDL.
---

Before writing a CREATE IMAGE REPOSITORY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE IMAGE REPOSITORY IF NOT EXISTS`.
5. The ENCRYPTION parameter cannot be changed after creation — confirm the correct encryption type with the user if it matters for their security posture (e.g., Tri-Secret Secure requires SNOWFLAKE_FULL).
6. Repository identifiers do not support quoted names; ensure the name uses only alphanumeric characters and underscores.
