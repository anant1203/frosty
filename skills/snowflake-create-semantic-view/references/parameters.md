# CREATE SEMANTIC VIEW — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view
(Snowflake feature introduced 2024–2025; built from Snowflake training knowledge and official documentation.)

---

## Full Syntax

```sql
CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  TABLES ( <logicalTable> [ , ... ] )
  [ RELATIONSHIPS ( <relationshipDef> [ , ... ] ) ]
  [ FACTS ( <factExpression> [ , ... ] ) ]
  [ DIMENSIONS ( <dimensionExpression> [ , ... ] ) ]
  [ METRICS ( { <metricExpression> | <windowFunctionMetricExpression> } [ , ... ] ) ]
  [ COMMENT = '<comment_about_semantic_view>' ]
  [ AI_SQL_GENERATION '<instructions_for_sql_generation>' ]
  [ AI_QUESTION_CATEGORIZATION '<instructions_for_question_categorization>' ]
  [ COPY GRANTS ]
```

### Logical Table Definition (`logicalTable`)

```sql
<alias> AS <db>.<schema>.<table_or_view>
  [ PRIMARY KEY ( <col_name> [, ...] ) ]
  [ UNIQUE ( <col_name> [, ...] ) ]
  [ CONSTRAINT <constraint_name> ... ]
  [ COMMENT = '<table_comment>' ]
```

### Relationship Definition (`relationshipDef`)

```sql
<left_table_alias> JOIN <right_table_alias>
  ON <left_table_alias>.<col> = <right_table_alias>.<col>
  [ JOIN TYPE { INNER | LEFT | RIGHT | FULL } ]
  [ ASOF MATCH_CONDITION <condition> ]
  [ RANGE BETWEEN ... ]
```

### Fact Expression (`factExpression`)

```sql
<alias>.<col_name> [ AS <logical_col_name> ]
  [ { PRIVATE | PUBLIC } ]
  [ COMMENT = '<column_comment>' ]
```

### Dimension Expression (`dimensionExpression`)

```sql
<alias>.<col_name> [ AS <logical_col_name> ]
  [ COMMENT = '<column_comment>' ]
```
Dimensions are always PUBLIC.

### Metric Expression (`metricExpression`)

```sql
<metric_name> AS <aggregate_expression>
  [ COMMENT = '<metric_comment>' ]
```

### Window Function Metric Expression (`windowFunctionMetricExpression`)

```sql
<metric_name> AS <window_function_expression>
  OVER ( [ PARTITION BY <dim_ref> [, ...] ] ORDER BY <dim_ref> )
  [ COMMENT = '<metric_comment>' ]
```

---

## Defaults Table

| Parameter | Default Value |
|---|---|
| `OR REPLACE` | Not set |
| `IF NOT EXISTS` | Not set |
| `RELATIONSHIPS` | None (no joins between logical tables) |
| `FACTS` | None |
| `DIMENSIONS` | None (but at least DIMENSIONS or METRICS is required) |
| `METRICS` | None (but at least DIMENSIONS or METRICS is required) |
| `COMMENT` | None |
| `AI_SQL_GENERATION` | None |
| `AI_QUESTION_CATEGORIZATION` | None |
| `COPY GRANTS` | Not set (inherits future grants only) |
| Dimension visibility | Always `PUBLIC` |
| Fact visibility | `PUBLIC` unless marked `PRIVATE` |

---

## Parameter Descriptions

### `name`
Identifier for the Semantic View. Must be unique within the schema. Must start with an alphabetic character. Use double-quoted identifiers for case-sensitive or special-character names.

### `TABLES ( logicalTable [, ...] )`
**Required.** Defines the logical tables that make up the semantic layer. Each entry maps an alias to a physical Snowflake table or view in the format `<alias> AS <db>.<schema>.<object>`. Aliases are used throughout `RELATIONSHIPS`, `FACTS`, `DIMENSIONS`, and `METRICS` to reference columns. Optional sub-clauses:
- `PRIMARY KEY (col_name [, ...])` — declares the primary key columns; used by the query engine to optimize joins.
- `UNIQUE (col_name [, ...])` — declares unique key columns.
- `CONSTRAINT` — named constraint definitions.
- `COMMENT = '<text>'` — description of this logical table.

### `RELATIONSHIPS ( relationshipDef [, ...] )`
Optional. Defines how logical tables join to each other. Each relationship specifies a left table alias, a right table alias, a join condition, and optionally a join type. Three join patterns are supported:
- **Standard equi-join**: `LEFT_ALIAS JOIN RIGHT_ALIAS ON LEFT_ALIAS.col = RIGHT_ALIAS.col`
- **ASOF join**: time-based fuzzy matching using `ASOF MATCH_CONDITION`
- **Range join**: joins rows within a numeric or timestamp range using `RANGE BETWEEN`

### `FACTS ( factExpression [, ...] )`
Optional. Declares computed or raw column values that represent measurable business facts (e.g., revenue, quantity). Each fact expression references a column from a logical table alias and may assign a logical name via `AS`. Facts may be marked `PRIVATE` (hidden from end users, usable only within METRICS expressions) or `PUBLIC` (visible and queryable).

### `DIMENSIONS ( dimensionExpression [, ...] )`
Optional, but required unless `METRICS` is also present. Declares categorical or descriptive attributes (e.g., region, product name, date). Each dimension references a column from a logical table alias and may have a `COMMENT`. All dimensions are `PUBLIC`.

### `METRICS ( metricExpression | windowFunctionMetricExpression [, ...] )`
Optional, but required unless `DIMENSIONS` is also present. Declares aggregated business metrics derived from facts and dimensions. Two sub-forms:
- **Aggregate metric**: `metric_name AS aggregate_expression` — e.g., `total_revenue AS SUM(orders.revenue)`
- **Window function metric**: supports non-additive computations (e.g., running totals, rank, lag) using standard SQL window functions with an explicit `OVER` clause referencing dimensions.

### `COMMENT`
Optional free-text description of the semantic view. Visible in `SHOW SEMANTIC VIEWS` and `DESCRIBE SEMANTIC VIEW`.

### `AI_SQL_GENERATION '<instructions>'`
Optional natural-language instructions that guide Cortex Analyst when generating SQL queries from the semantic view. Use to specify preferred join paths, aggregation defaults, date grain conventions, or business rules that are not captured structurally. Example: `'Always aggregate revenue by calendar month. Use the orders table as the primary fact source.'`

### `AI_QUESTION_CATEGORIZATION '<instructions>'`
Optional natural-language instructions that guide Cortex Analyst when classifying or routing user questions. Use to define question categories (e.g., "finance questions", "operational questions") and how each should be interpreted against this semantic view.

### `COPY GRANTS`
When used with `OR REPLACE`, transfers the existing privilege grants from the previous version of the semantic view to the replacement. Without this clause only future grants are inherited.

---

## Usage Notes

- Semantic Views are the primary input artifact for Cortex Analyst (`SNOWFLAKE.CORTEX.ANALYST` function).
- A Semantic View does not store or materialize data; it is a metadata object describing the semantic layer over physical tables.
- At least one of `DIMENSIONS` or `METRICS` must be present; a view with only `TABLES` and `RELATIONSHIPS` is not valid.
- Cortex Analyst uses `AI_SQL_GENERATION` instructions at query time to resolve ambiguity in natural-language questions.
- Privilege required to create: `CREATE SEMANTIC VIEW` on the target schema.
- Privilege required to query via Cortex Analyst: `USAGE` on the semantic view object.
