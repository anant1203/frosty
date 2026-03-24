---
name: snowflake-create-notebook
description: Consult Snowflake CREATE NOTEBOOK parameter reference before generating any CREATE NOTEBOOK DDL.
---

Before writing a CREATE NOTEBOOK statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE NOTEBOOK IF NOT EXISTS` where supported.
5. Choose the correct runtime: use `RUNTIME_NAME = 'SYSTEM$WAREHOUSE_RUNTIME'` (the default) unless the user explicitly needs Container Runtime (GPU workloads or containerised environments). Container Runtime requires `COMPUTE_POOL` to be set and does not use `QUERY_WAREHOUSE` for compute. Always pair `COMPUTE_POOL` with a Container Runtime `RUNTIME_NAME`.
6. `QUERY_WAREHOUSE` is required when the notebook will be executed via `EXECUTE NOTEBOOK`; omit it only if the user's workflow never calls that command.
7. `IDLE_AUTO_SHUTDOWN_TIME_SECONDS` only applies to Container Runtime notebooks; do not emit it for Warehouse Runtime notebooks.
