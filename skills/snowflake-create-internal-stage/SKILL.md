---
name: snowflake-create-internal-stage
description: Consult Snowflake CREATE STAGE parameter reference before generating any CREATE STAGE DDL for internal stages.
---

Before writing a CREATE STAGE statement for an internal stage:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE STAGE IF NOT EXISTS`.
5. Named internal stages are the correct choice for sharing data across multiple tables or users within an account; use user stages (@~) or table stages (@%table) only when the user explicitly requests them (they cannot be created with DDL).
6. The default encryption for internal named stages is `SNOWFLAKE_FULL` (client-side + server-side). Use `SNOWFLAKE_SSE` only when the user explicitly wants server-side-only encryption.
7. Attach a FILE_FORMAT only when the user specifies a non-CSV format or custom format options; omit otherwise to rely on COPY INTO defaults.
8. Enable the DIRECTORY table (`DIRECTORY = ( ENABLE = TRUE )`) only when the user needs to browse or query staged files via directory table functions.
