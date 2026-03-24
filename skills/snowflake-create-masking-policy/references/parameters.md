# Snowflake CREATE MASKING POLICY — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] MASKING POLICY [ IF NOT EXISTS ] <name> AS
( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )
RETURNS <arg_type_to_mask> -> <body>
[ COMMENT = '<string_literal>' ]
[ EXEMPT_OTHER_POLICIES = { TRUE | FALSE } ]
```

---

## Parameter Defaults

| Parameter              | Default | Notes                                                                           |
|------------------------|---------|---------------------------------------------------------------------------------|
| COMMENT                | (none)  | Free-text description                                                           |
| EXEMPT_OTHER_POLICIES  | FALSE   | Cannot be changed once policy is attached to a table or view                   |

---

## Required Parameters

### `<name>`
Unique identifier for the masking policy within the schema. Must begin with an alphabetic character. Special characters and spaces require double quotes (identifiers in quotes are case-sensitive).

---

### `AS ( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )`
The policy **signature** — defines the input arguments evaluated at query runtime.

- **First argument** (`<arg_name_to_mask> <arg_type_to_mask>`): Represents the column whose data will be masked or tokenized. The data type here determines the required `RETURNS` type.
- **Additional arguments** (`<arg_1> <arg_type_1> ...`): Optional context columns used for conditional logic (e.g. a role column, a sensitivity flag). These cannot be virtual columns.
- The argument names are local to the policy body and do not need to match the actual column names in the table.

```sql
-- Simple policy (one argument)
AS (val STRING)

-- Conditional policy (multiple arguments)
AS (val STRING, sensitivity STRING)
```

---

### `RETURNS <arg_type_to_mask>`
The return data type of the policy body.

- **Must exactly match** the data type of the first argument.
- Cross-type transformations are not allowed (e.g. cannot mask a `NUMBER` and return `STRING`).

---

### `<body>`
SQL expression that transforms the masked column's value. Evaluated at query time for each row.

Common patterns:

```sql
-- Hash the value for non-privileged roles
-> CASE
     WHEN CURRENT_ROLE() IN ('ANALYST') THEN SHA2(val)
     ELSE val
   END

-- Partially redact email
-> CASE
     WHEN IS_ROLE_IN_SESSION('DATA_STEWARD') THEN val
     ELSE REGEXP_REPLACE(val, '.+\@', '***@')
   END

-- Always mask (full redaction)
-> '*** REDACTED ***'
```

Valid body components:
- Conditional functions: `CASE`, `IFF`, `DECODE`
- Built-in masking/hashing functions: `SHA2`, `MD5`, `REGEXP_REPLACE`, `MASK`
- Context functions: `CURRENT_ROLE()`, `IS_ROLE_IN_SESSION()`, `CURRENT_USER()`
- User-defined functions (UDFs) and external functions

---

## Optional Parameters

### `COMMENT = '<string_literal>'`
Free-text description for the masking policy.

- **Default:** (none)

---

### `EXEMPT_OTHER_POLICIES = { TRUE | FALSE }`
Controls whether this masking policy's protected column can be referenced by row access policies or other conditional masking policies.

| Value  | Behaviour                                                                                              |
|--------|--------------------------------------------------------------------------------------------------------|
| `TRUE` | Row access policies and other conditional masking policies may reference the protected column          |
| `FALSE` | Row access policies and other conditional masking policies cannot reference the protected column (default) |

- **Default:** `FALSE`
- **Critical constraint:** This value cannot be changed after the policy is attached to any table or view. Set it correctly at creation time.
- **Use when:** The policy must interoperate with row access policies (e.g. a row access policy filters rows based on a column that is itself masked).

---

## Access Control Requirements
- `CREATE MASKING POLICY` privilege on the schema.
- `APPLY MASKING POLICY` privilege to attach the policy to a table or view column.

---

## Constraints & Notes
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- `CREATE OR REPLACE` is atomic — the old object is dropped and the new one created in a single transaction.
- Input and output data types must match exactly; there is no implicit type casting.
- Virtual columns cannot serve as the first argument in a conditional masking policy.
- A single masking policy can be applied to multiple columns, but each column can only have one masking policy active at a time.
- Masking policies are evaluated **after** row access policies filter rows.
