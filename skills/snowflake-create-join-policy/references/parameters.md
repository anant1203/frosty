# CREATE JOIN POLICY — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-join-policy

## Syntax

```sql
CREATE [ OR REPLACE ] JOIN POLICY [ IF NOT EXISTS ] <name>
  AS () RETURNS JOIN_CONSTRAINT -> <body>
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| body | — (required) |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the join policy within the schema. Must begin with an alphabetic character; enclose in double quotes if the name contains spaces or special characters. Double-quoted identifiers are case-sensitive.

### `AS () RETURNS JOIN_CONSTRAINT` (required)
The fixed signature and return type of the policy. The signature accepts no arguments; the return type is `JOIN_CONSTRAINT`, which is an internal Snowflake data type.

### `<body>` (required)
An SQL expression that determines the join restrictions applied when a query accesses a table or view assigned this policy. The body must call the `JOIN_CONSTRAINT` function.

#### `JOIN_CONSTRAINT(JOIN_REQUIRED => <boolean_expression>)`

```sql
JOIN_CONSTRAINT (
  { JOIN_REQUIRED => <boolean_expression> }
)
```

Parameters:
- `JOIN_REQUIRED` — A boolean expression that determines whether a join is required.
  - `TRUE` — Queries selecting from the protected table/view must join to another table or view. Queries without a join are rejected.
  - `FALSE` — No join is required; queries may select data without joining. This is effectively equivalent to no policy.

```sql
-- Example body: always require a join
JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)

-- Example body: no restriction
JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE)
```

### `COMMENT`
A descriptive string for the join policy. Default: none.

## Constraints and Notes

- The policy body cannot reference user-defined functions, tables, or views.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- `CREATE OR REPLACE` operations are atomic transactions.
- The **allowed join columns** (which columns must be used in the join predicate) are specified when assigning the policy to a table or view, not in the CREATE statement:
  ```sql
  ALTER TABLE <table_name> SET JOIN POLICY <policy_name>
    ALLOWED_JOIN_KEYS = ( <column_1> [, <column_2> ...] );
  ```
