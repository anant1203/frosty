---
name: snowflake-create-user
description: Consult Snowflake CREATE USER parameter reference before generating any CREATE USER DDL.
---

Before writing a CREATE USER statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE USER IF NOT EXISTS`.
5. Always set `TYPE` explicitly when creating service accounts (TYPE = SERVICE) vs human users (TYPE = PERSON). Never set a PASSWORD for SERVICE type users; use key-pair authentication (RSA_PUBLIC_KEY) instead. If MUST_CHANGE_PASSWORD is applicable, set it to TRUE for new human users receiving an initial password. Always set DEFAULT_ROLE, DEFAULT_WAREHOUSE, and DEFAULT_NAMESPACE when known, as omitting them leaves the user with no usable session context on first login.
