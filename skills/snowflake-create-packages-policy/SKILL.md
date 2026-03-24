---
name: snowflake-create-packages-policy
description: Consult Snowflake CREATE PACKAGES POLICY parameter reference before generating any CREATE PACKAGES POLICY DDL.
---

Before writing a CREATE PACKAGES POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE PACKAGES POLICY IF NOT EXISTS`.
5. `LANGUAGE PYTHON` is the only supported language and is always required.
6. Package specs follow the format `package_name==version` or `package_name` (wildcard version). Use `*` in ALLOWLIST to allow all packages (the default); be explicit when restricting to specific packages.
7. ADDITIONAL_CREATION_BLOCKLIST restricts packages at UDF/procedure creation time in addition to runtime; use this for packages that should never appear in any code even temporarily.
