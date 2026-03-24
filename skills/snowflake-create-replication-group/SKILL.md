---
name: snowflake-create-replication-group
description: Consult Snowflake CREATE REPLICATION GROUP parameter reference before generating any CREATE REPLICATION GROUP DDL.
---

Before writing a CREATE REPLICATION GROUP statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE REPLICATION GROUP IF NOT EXISTS`.
5. Use the primary group syntax when creating in the source account; use the secondary (AS REPLICA OF) syntax when creating in a target account.
6. `OBJECT_TYPES` is required — always confirm which object types the user wants to replicate.
7. When DATABASES is in OBJECT_TYPES, `ALLOWED_DATABASES` is also required. Similarly, `ALLOWED_SHARES` is required when SHARES is included, `ALLOWED_EXTERNAL_VOLUMES` for EXTERNAL VOLUMES, and `ALLOWED_INTEGRATION_TYPES` for INTEGRATIONS.
8. `ALLOWED_ACCOUNTS` is required and must use `org_name.account_name` format.
9. Unlike failover groups, replication groups do not support automatic failover — clarify this distinction if the user's intent is high availability.
