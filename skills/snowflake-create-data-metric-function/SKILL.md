---
name: snowflake-create-data-metric-function
description: Consult Snowflake CREATE DATA METRIC FUNCTION parameter reference before generating any CREATE DATA METRIC FUNCTION DDL.
---

Before writing a CREATE DATA METRIC FUNCTION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE DATA METRIC FUNCTION IF NOT EXISTS` where supported.
5. The function body must be a deterministic SQL expression that returns a scalar NUMBER; avoid nondeterministic functions such as CURRENT_TIME or RANDOM.
6. The table argument signature must list every column that the expression references; all listed columns must belong to the same table.
7. Mark the function `SECURE` when the expression logic or column names would reveal sensitive business rules to non-owner roles.
8. Use `$$` delimiters for the AS clause when the expression body contains single-quote characters.
