---
name: snowflake-create-hybrid-table
description: Consult Snowflake CREATE HYBRID TABLE parameter reference before generating any CREATE HYBRID TABLE DDL.
---

Before writing a CREATE HYBRID TABLE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE HYBRID TABLE IF NOT EXISTS` where supported.
5. A `PRIMARY KEY` constraint is mandatory — always include it. It may be defined inline on a single column or as an out-of-line constraint for composite keys.
6. `PRIMARY KEY`, `UNIQUE`, and `FOREIGN KEY` constraints are enforced at the row level; do not set `NOT ENFORCED` on any constraint.
7. Do not apply `COLLATE` to primary key or indexed columns — collation is not supported on those columns.
8. Hybrid tables cannot be `TEMPORARY` or `TRANSIENT`; do not include those modifiers.
9. Hybrid tables are only available in AWS and Azure commercial regions; note this if the user's account region is relevant.
10. Use `AUTOINCREMENT`/`IDENTITY` with `NOORDER` for better point-write performance when the user needs a surrogate key.
