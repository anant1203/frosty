---
name: snowflake-create-connection
description: Consult Snowflake CREATE CONNECTION parameter reference before generating any CREATE CONNECTION DDL.
---

Before writing a CREATE CONNECTION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE CONNECTION IF NOT EXISTS`.
5. Use the primary connection syntax when creating a new connection; use the secondary syntax (`AS REPLICA OF`) when creating a secondary connection to replicate an existing primary.
6. For secondary connections, the name must match the primary connection's name exactly.
7. Connection names must be unique across all connection and account names in the organization — verify this constraint.
8. Only ACCOUNTADMIN can execute CREATE CONNECTION — note this privilege requirement.
