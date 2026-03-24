---
name: snowflake-create-password-policy
description: Consult Snowflake CREATE PASSWORD POLICY parameter reference before generating any CREATE PASSWORD POLICY DDL.
---

Before writing a CREATE PASSWORD POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE PASSWORD POLICY IF NOT EXISTS`.
5. Ensure PASSWORD_MIN_LENGTH is always less than or equal to PASSWORD_MAX_LENGTH; flag any contradiction to the user before generating DDL.
6. When the user asks for a "strict" policy, suggest increasing PASSWORD_MIN_SPECIAL_CHARS, PASSWORD_MIN_UPPER_CASE_CHARS, PASSWORD_MIN_NUMERIC_CHARS, and reducing PASSWORD_MAX_AGE_DAYS and PASSWORD_MAX_RETRIES.
7. PASSWORD_HISTORY prevents recent-password reuse; remind users this does not apply retroactively to existing passwords.
