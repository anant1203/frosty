---
name: snowflake-create-authentication-policy
description: Consult Snowflake CREATE AUTHENTICATION POLICY parameter reference before generating any CREATE AUTHENTICATION POLICY DDL.
---

Before writing a CREATE AUTHENTICATION POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE AUTHENTICATION POLICY IF NOT EXISTS`.
5. When the user specifies MFA requirements, select MFA_ENROLLMENT carefully: use `REQUIRED` to force all users and `REQUIRED_PASSWORD_ONLY` only for password-based logins. Omit if leaving the default `OPTIONAL` behavior.
6. For SECURITY_INTEGRATIONS, only list specific integration names when the user's SAML or OAuth setup is known; otherwise leave as the default `ALL`.
7. When configuring PAT_POLICY or WORKLOAD_IDENTITY_POLICY, always include each sub-property explicitly rather than relying on nested defaults.
