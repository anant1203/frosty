---
name: snowflake-create-warehouse
description: Consult Snowflake CREATE WAREHOUSE parameter reference before generating any CREATE WAREHOUSE DDL.
---

Before writing a CREATE WAREHOUSE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE WAREHOUSE IF NOT EXISTS`.
5. Always set AUTO_SUSPEND explicitly (recommended: 60–300 seconds for interactive warehouses, higher for batch). Set INITIALLY_SUSPENDED = TRUE for warehouses that should not start billing immediately. For multi-cluster warehouses, set both MIN_CLUSTER_COUNT and MAX_CLUSTER_COUNT and always specify SCALING_POLICY. Use WAREHOUSE_SIZE = XSMALL as the starting point unless the workload clearly demands a larger size. Assign a RESOURCE_MONITOR when the warehouse has a defined cost budget.
