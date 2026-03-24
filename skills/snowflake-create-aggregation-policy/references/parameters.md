# CREATE AGGREGATION POLICY — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-aggregation-policy

## Syntax

```sql
CREATE [ OR REPLACE ] AGGREGATION POLICY [ IF NOT EXISTS ] <name>
  AS () RETURNS AGGREGATION_CONSTRAINT -> <body>
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| body | — (required) |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the aggregation policy within the schema. Must begin with an alphabetic character; enclose in double quotes if the name contains spaces or special characters. Double-quoted identifiers are case-sensitive.

### `AS () RETURNS AGGREGATION_CONSTRAINT` (required)
The fixed signature and return type of the policy. The signature accepts no arguments; the return type is `AGGREGATION_CONSTRAINT`, which is an internal Snowflake data type.

### `<body>` (required)
An SQL expression defining the aggregation restrictions. The body must call exactly one of the following built-in constraint functions:

#### `NO_AGGREGATION_CONSTRAINT()`
Returns unrestricted access to tables and views assigned this policy. Equivalent to having no policy — users can query the data without aggregation requirements.

```sql
-- Example body: no restriction
NO_AGGREGATION_CONSTRAINT()
```

#### `AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => <integer_expression>)`
Requires that query results be aggregated, with each aggregation group containing at least the specified minimum number of rows.

Parameters:
- `MIN_GROUP_SIZE` — The minimum number of rows per aggregation group.
  - Value `1` — each group must contain at least one row from the constrained table.
  - Value `0` — groups may consist entirely of rows from other (non-constrained) tables.
  - Higher values enforce stronger k-anonymity guarantees.

```sql
-- Example body: require at least 5 rows per group
AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5)
```

### `COMMENT`
A descriptive string for the aggregation policy. Default: none.

## Constraints and Notes

- The policy body cannot reference user-defined functions, tables, or views.
- Aggregation policies require **Snowflake Enterprise Edition** or higher.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Apply the policy to a table or view with: `ALTER TABLE <name> SET AGGREGATION POLICY <policy_name>`
