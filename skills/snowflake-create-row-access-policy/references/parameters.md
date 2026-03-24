# Snowflake CREATE ROW ACCESS POLICY — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] ROW ACCESS POLICY [ IF NOT EXISTS ] <name> AS
( <arg_name> <arg_type> [ , <arg_name_n> <arg_type_n> ... ] )
RETURNS BOOLEAN -> <body>
[ COMMENT = '<string_literal>' ]
```

---

## Parameter Defaults

| Parameter | Default | Notes                             |
|-----------|---------|-----------------------------------|
| COMMENT   | (none)  | Free-text description             |

---

## Required Parameters

### `<name>`
Unique identifier for the row access policy within the schema. Must begin with an alphabetic character. Special characters and spaces require double quotes (identifiers in quotes are case-sensitive).

---

### `AS ( <arg_name> <arg_type> [ , ... ] )`
The policy **signature** — defines the columns from the protected table/view that are evaluated at query runtime to decide row visibility.

- Each argument maps to a column in the table or view the policy will be attached to.
- Argument names are local to the policy body; they do not need to match the actual column names.
- The signature **cannot be modified** once the policy is attached to any table or view.
- At least one argument is required.

```sql
-- Single-column signature
AS (region_code STRING)

-- Multi-column signature
AS (user_id STRING, data_classification STRING)
```

---

### `RETURNS BOOLEAN`
The policy must always return a boolean value.

- `TRUE` — the row is visible to the querying user/role.
- `FALSE` — the row is hidden (filtered out of results).

---

### `<body>`
SQL expression that evaluates to `TRUE` or `FALSE` for each row.

**Simple role-based filter:**
```sql
-> CASE
     WHEN CURRENT_ROLE() = 'ADMIN' THEN TRUE
     WHEN region_code = GET(PARSE_JSON(CURRENT_SESSION_USER_CONTEXT()), 'region') THEN TRUE
     ELSE FALSE
   END
```

**Lookup table pattern:**
```sql
-> EXISTS (
     SELECT 1 FROM access_control_table act
     WHERE act.user = CURRENT_USER()
       AND act.allowed_region = region_code
   )
```

**Always-allow (useful as a placeholder):**
```sql
-> TRUE
```

Valid body components:
- Conditional expressions: `CASE`, `IFF`, `DECODE`
- Context functions: `CURRENT_ROLE()`, `IS_ROLE_IN_SESSION()`, `CURRENT_USER()`, `CURRENT_ACCOUNT()`
- Subqueries referencing lookup/mapping tables (use sparingly — see constraints)
- User-defined functions (UDFs) and external functions

---

## Optional Parameters

### `COMMENT = '<string_literal>'`
Free-text description for the row access policy.

- **Default:** (none)

---

## Access Control Requirements
- `CREATE ROW ACCESS POLICY` privilege on the schema.
- `APPLY ROW ACCESS POLICY` privilege to attach the policy to a table or view.
- Enterprise Edition or higher recommended (available in Business Critical for some features).

---

## Constraints & Notes
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- `CREATE OR REPLACE` is atomic — the old object is dropped and the new one created in a single transaction.
- The policy signature **cannot be altered** while the policy is attached to any table or view. To change the signature, detach the policy first, then recreate it.
- Row access policies are evaluated **before** masking policies; design the logic accordingly when both types are applied to the same table.
- The same column cannot appear in both a row access policy signature and a masking policy signature on the same table.
- Complex subqueries in the body may cause runtime errors in certain query plans; prefer simple lookups and minimize subquery depth.
- Data sharing providers cannot create row access policies in reader accounts.
- A table or view can have at most one row access policy attached at a time.
