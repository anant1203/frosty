---
name: snowflake-create-sequence
description: Consult Snowflake CREATE SEQUENCE parameter reference before generating any CREATE SEQUENCE DDL.
---

Before writing a CREATE SEQUENCE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE SEQUENCE IF NOT EXISTS` where supported.
5. Warn users that Snowflake does not guarantee gap-free sequence values; sequences are not suitable for gapless numbering requirements.
6. The `START` value cannot be modified after creation; confirm the correct starting value before generating DDL.
7. Use `ORDER` only when strictly sequential values are required; `NOORDER` (the default for most accounts) offers better concurrency performance.
