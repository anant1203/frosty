---
name: snowflake-create-secret
description: Consult Snowflake CREATE SECRET parameter reference before generating any CREATE SECRET DDL.
---

Before writing a CREATE SECRET statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE SECRET IF NOT EXISTS`.
5. Select the correct TYPE based on the use case:
   - `GENERIC_STRING` for API tokens or arbitrary sensitive strings accessed via `SYSTEM$GET_SECRET`.
   - `PASSWORD` for username/password basic-auth credentials.
   - `OAUTH2` with `API_AUTHENTICATION` + `OAUTH_SCOPES` for OAuth2 client-credentials flow.
   - `OAUTH2` with `OAUTH_REFRESH_TOKEN` + `OAUTH_REFRESH_TOKEN_EXPIRY_TIME` + `API_AUTHENTICATION` for OAuth2 authorization-code-grant flow.
6. The secret value (SECRET_STRING, PASSWORD, OAUTH_REFRESH_TOKEN) is never shown after creation; advise users to store the original value securely.
7. For OAUTH2 secrets, the referenced security integration must exist and its OAUTH_ALLOWED_SCOPES must cover any requested OAUTH_SCOPES.
