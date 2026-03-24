---
name: snowflake-create-view
description: Consult Snowflake CREATE VIEW parameter reference before generating any CREATE VIEW DDL.
---

Before writing a CREATE VIEW statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE VIEW IF NOT EXISTS`.
5. Add the SECURE keyword only when the user explicitly needs to restrict access to the view definition (e.g. hiding business logic from non-privileged users).
6. Use TEMPORARY/TEMP/VOLATILE only when the view is needed for session-scoped intermediate work; it will be dropped automatically at session end.
7. Use RECURSIVE only when the SELECT statement needs to reference the view itself (self-referencing query); provide an explicit column list when RECURSIVE is used.
8. Enable CHANGE_TRACKING = TRUE only when the user needs to create a stream on this view or track row-level changes.
9. Views share the namespace with tables — a view and a table cannot have the same name within a schema.
10. The SELECT statement is limited to 95 KB; all columns derived from expressions must be given explicit aliases.
