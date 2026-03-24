---
name: snowflake-create-external-function
description: Consult Snowflake CREATE EXTERNAL FUNCTION parameter reference before generating any CREATE EXTERNAL FUNCTION DDL.
---

Before writing a CREATE EXTERNAL FUNCTION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE EXTERNAL FUNCTION IF NOT EXISTS` where supported (note: IF NOT EXISTS is not supported for external functions — omit it and warn the user).
5. `API_INTEGRATION` and the `AS '<url>'` clause are always required; ensure both are present.
6. Set `MAX_BATCH_ROWS` explicitly when the remote service has a documented row-per-request limit.
7. Use `RETURNS NULL ON NULL INPUT` when the remote endpoint cannot handle NULL payloads.
8. Prefer `COMPRESSION = NONE` during development to simplify payload inspection; switch to `AUTO` (default) for production.
9. Use `REQUEST_TRANSLATOR` / `RESPONSE_TRANSLATOR` UDFs to adapt the Snowflake row-array envelope to/from custom API schemas.
