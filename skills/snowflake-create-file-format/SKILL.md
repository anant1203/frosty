---
name: snowflake-create-file-format
description: Consult Snowflake CREATE FILE FORMAT parameter reference before generating any CREATE FILE FORMAT DDL.
---

Before writing a CREATE FILE FORMAT statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE FILE FORMAT IF NOT EXISTS`.
5. Always specify the `TYPE` parameter explicitly, even though CSV is the default, to make the format self-documenting.
6. For CSV formats, pay special attention to `FIELD_OPTIONALLY_ENCLOSED_BY`, `NULL_IF`, `SKIP_HEADER`, and `COMPRESSION` — these are the most commonly customized options.
7. AVRO, ORC, and XML formats are for loading only; do not use them for unloading.
8. Do not combine `OR REPLACE` and `IF NOT EXISTS` in the same statement — they are mutually exclusive.
