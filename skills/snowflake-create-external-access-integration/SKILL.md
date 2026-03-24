---
name: snowflake-create-external-access-integration
description: Consult Snowflake CREATE EXTERNAL ACCESS INTEGRATION parameter reference before generating any CREATE EXTERNAL ACCESS INTEGRATION DDL.
---

Before writing a CREATE EXTERNAL ACCESS INTEGRATION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — use `CREATE EXTERNAL ACCESS INTEGRATION` (IF NOT EXISTS is not supported for this object).
5. ALLOWED_NETWORK_RULES must reference EGRESS-mode network rules only; INGRESS or INTERNAL_STAGE rules will cause an error.
6. ALLOWED_AUTHENTICATION_SECRETS should be `none` unless the external endpoint requires authentication; when secrets are needed, list them explicitly rather than using `all`.
7. ENABLED = TRUE is the default; only include it explicitly if setting to FALSE or the user wants the integration disabled at creation time.
