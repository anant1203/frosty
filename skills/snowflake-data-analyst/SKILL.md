---
name: snowflake-data-analyst
description: Business rules and domain knowledge for answering natural-language data questions accurately against Snowflake.
---

Before generating SQL for any data question:

1. Read `references/business-rules.md` to load domain context — metric definitions,
   canonical column names, standard filters, common join paths, and date conventions.

2. Apply any relevant rules when writing the SQL:
   - Use the exact column and calculation defined for each metric (e.g. "revenue" may
     map to `SUM(ORDER_VALUE) WHERE STATUS = 'COMPLETED'`, not a raw column sum).
   - Apply standard filters listed in the rules (e.g. exclude test records, restrict
     to active statuses) unless the user explicitly asks to include them.
   - Use the documented join keys when combining tables — do not guess join columns
     from column name similarity alone.
   - Filter on the canonical date column per table (e.g. always filter ORDERS on
     ORDER_DATE, not CREATED_AT) unless the user specifies otherwise.

3. If the user's question references a term defined in the business rules, always
   use the rule definition — do not derive it from column names alone.

4. If the business-rules.md file is empty or has only template placeholders, skip
   this step and fall back to schema context from discover_schema.

5. If no rule applies to part of the question, use schema context and reasonable
   Snowflake defaults.
