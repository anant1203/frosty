---
name: snowflake-create-compute-pool
description: Consult Snowflake CREATE COMPUTE POOL parameter reference before generating any CREATE COMPUTE POOL DDL.
---

Before writing a CREATE COMPUTE POOL statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE COMPUTE POOL IF NOT EXISTS`.
5. Always set MIN_NODES, MAX_NODES, and INSTANCE_FAMILY — these are required. Choose INSTANCE_FAMILY based on workload: CPU_X64_XS/S/M/L for general workloads, HIGHMEM_X64_S/M/L for memory-intensive workloads, GPU_NV_S/M/L for GPU workloads. Set INITIALLY_SUSPENDED = TRUE for pools that should not incur cost immediately. Set AUTO_SUSPEND_SECS conservatively (default 3600) to avoid runaway costs. Use FOR APPLICATION only when the pool is dedicated to a Snowflake Native App.
