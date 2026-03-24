---
name: snowflake-create-application-package
description: Consult Snowflake CREATE APPLICATION PACKAGE parameter reference before generating any CREATE APPLICATION PACKAGE DDL.
---

Before writing a CREATE APPLICATION PACKAGE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE APPLICATION PACKAGE IF NOT EXISTS` where supported.
5. Always ask the provider whether the package is for internal (intra-organization) or external (cross-organization/Snowflake Marketplace) distribution and set `DISTRIBUTION` accordingly. Setting `DISTRIBUTION = EXTERNAL` triggers an automated Snowflake security review; warn the user.
6. `MULTIPLE_INSTANCES = TRUE` and `ENABLE_RELEASE_CHANNELS = TRUE` are irreversible once set — prompt the user to confirm before including either flag.
7. `DATA_RETENTION_TIME_IN_DAYS` is bounded by account edition: Standard (0–1), Enterprise (0–90); validate the user's value against their edition before emitting the DDL.
