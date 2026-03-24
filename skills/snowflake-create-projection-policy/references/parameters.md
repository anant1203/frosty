# Snowflake CREATE PROJECTION POLICY — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] PROJECTION POLICY [ IF NOT EXISTS ] <name>
  AS () RETURNS PROJECTION_CONSTRAINT -> <body>
  [ COMMENT = '<string_literal>' ]
```

### `PROJECTION_CONSTRAINT` function signature (used inside `<body>`)

```sql
PROJECTION_CONSTRAINT(
    ALLOW       => { TRUE | FALSE }
  [, ENFORCEMENT => { 'FAIL' | 'NULLIFY' } ]
)
```

---

## Parameter Defaults

| Parameter   | Default  | Notes                                                            |
|-------------|----------|------------------------------------------------------------------|
| ENFORCEMENT | `'FAIL'` | Only relevant when `ALLOW => FALSE`                              |
| COMMENT     | (none)   | Free-text description                                            |

---

## Required Parameters

### `<name>`
Unique identifier for the projection policy within the schema. Must begin with an alphabetic character. Special characters and spaces require double quotes (identifiers in quotes are case-sensitive).

---

### `AS () RETURNS PROJECTION_CONSTRAINT`
Fixed signature for all projection policies. The argument list is always empty `()`. The return type is always `PROJECTION_CONSTRAINT`.

---

### `<body>`
SQL expression that calls `PROJECTION_CONSTRAINT(...)`. Determines whether the protected column may appear in a query's final result set.

**Allow all projection (pass-through):**
```sql
-> PROJECTION_CONSTRAINT(ALLOW => TRUE)
```

**Block projection — fail the query:**
```sql
-> PROJECTION_CONSTRAINT(ALLOW => FALSE)
```

**Block projection — return NULLs silently:**
```sql
-> PROJECTION_CONSTRAINT(ALLOW => FALSE, ENFORCEMENT => 'NULLIFY')
```

**Role-based conditional policy:**
```sql
-> CASE
     WHEN IS_ROLE_IN_SESSION('ANALYST')
       THEN PROJECTION_CONSTRAINT(ALLOW => FALSE, ENFORCEMENT => 'NULLIFY')
     ELSE PROJECTION_CONSTRAINT(ALLOW => TRUE)
   END
```

Supported context functions: `CURRENT_ROLE()`, `IS_ROLE_IN_SESSION()`, `CURRENT_USER()`.

---

## `PROJECTION_CONSTRAINT` Arguments

### `ALLOW => { TRUE | FALSE }` *(required)*
Controls whether the column may appear in the outermost `SELECT` list.

| Value   | Behaviour                                                                          |
|---------|------------------------------------------------------------------------------------|
| `TRUE`  | Column projection is allowed — the column value is returned normally               |
| `FALSE` | Column projection is blocked — behaviour depends on `ENFORCEMENT`                  |

- **Note:** `ALLOW => FALSE` only affects columns in the **final result set**. Columns used only in `WHERE`, `JOIN`, or `GROUP BY` clauses are not affected.

---

### `ENFORCEMENT => { 'FAIL' | 'NULLIFY' }` *(optional, only relevant when `ALLOW => FALSE`)*
Specifies how the system responds when a query attempts to project a blocked column.

| Value      | Behaviour                                                                 |
|------------|---------------------------------------------------------------------------|
| `'FAIL'`   | The query fails with an error when the protected column appears in the outermost SELECT (default) |
| `'NULLIFY'` | The query succeeds but every row returns NULL for the protected column   |

- **Default:** `'FAIL'`
- Choose `'NULLIFY'` only when the user explicitly needs silent nullification rather than hard query failures.

---

## Optional Top-Level Parameters

### `COMMENT = '<string_literal>'`
Free-text description for the projection policy.

- **Default:** (none)

---

## Access Control Requirements
- `CREATE PROJECTION POLICY` privilege on the schema.
- `APPLY PROJECTION POLICY` privilege to attach the policy to a column.
- Enterprise Edition or higher required.

---

## Constraints & Notes
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- `CREATE OR REPLACE` is atomic — the old object is dropped and the new one created in a single transaction.
- Projection policies only restrict columns in the **outermost** query's SELECT list; subquery projections are not blocked.
- A column can have at most one projection policy applied at a time.
- Projection policies are evaluated independently of masking and row access policies.
