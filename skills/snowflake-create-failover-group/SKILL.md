---
name: snowflake-create-failover-group
description: Consult Snowflake CREATE FAILOVER GROUP parameter reference before generating any CREATE FAILOVER GROUP DDL.
---

Before writing a CREATE FAILOVER GROUP statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE FAILOVER GROUP IF NOT EXISTS`.
5. Use the primary group syntax when creating in the source account; use the secondary (AS REPLICA OF) syntax when creating in a target account.
6. `OBJECT_TYPES` is required — always confirm which object types the user wants to replicate.
7. When DATABASES is in OBJECT_TYPES, `ALLOWED_DATABASES` is also required. Similarly, `ALLOWED_SHARES` is required when SHARES is included, `ALLOWED_EXTERNAL_VOLUMES` for EXTERNAL VOLUMES, and `ALLOWED_INTEGRATION_TYPES` for INTEGRATIONS.
8. `ALLOWED_ACCOUNTS` is required and must use `org_name.account_name` format.
9. This feature requires Business Critical Edition or higher — note this limitation when relevant.
