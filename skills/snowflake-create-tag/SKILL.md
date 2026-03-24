---
name: snowflake-create-tag
description: Consult Snowflake CREATE TAG parameter reference before generating any CREATE TAG DDL.
---

Before writing a CREATE TAG statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE TAG IF NOT EXISTS`.
5. If the user wants to restrict tag values to a specific set, include `ALLOWED_VALUES` and list it before all other optional parameters.
6. Only include `PROPAGATE` and `ON_CONFLICT` if the user explicitly requires automatic tag propagation (Enterprise Edition feature).
7. Tag names must start with an alphabetic character; enclose names with spaces or special characters in double quotes.
8. Do not place any sensitive, regulated, or personal data in the tag name, allowed values, or comment.
