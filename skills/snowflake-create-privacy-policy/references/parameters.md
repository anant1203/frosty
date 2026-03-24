# Snowflake CREATE PRIVACY POLICY — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] PRIVACY POLICY [ IF NOT EXISTS ] <name>
  AS () RETURNS PRIVACY_BUDGET -> <body>
  [ COMMENT = '<string_literal>' ]
```

### Privacy Budget function signature (used inside `<body>`)

```sql
PRIVACY_BUDGET(
    BUDGET_NAME              => '<string>'
  [, BUDGET_LIMIT            => <decimal> ]
  [, MAX_BUDGET_PER_AGGREGATE => <decimal> ]
  [, BUDGET_WINDOW           => '<window>' ]
)
```

### No-restriction function (used inside `<body>`)

```sql
NO_PRIVACY_POLICY()
```

---

## Parameter Defaults

| Parameter               | Default    | Notes                                                              |
|-------------------------|------------|--------------------------------------------------------------------|
| BUDGET_LIMIT            | 233.0      | Total privacy loss (epsilon) allowed per window; decimal > 0      |
| MAX_BUDGET_PER_AGGREGATE | 0.5       | Max epsilon consumed per individual aggregate query; decimal > 0  |
| BUDGET_WINDOW           | `'Weekly'` | Valid: `'Daily'`, `'Weekly'`, `'Monthly'`, `'Yearly'`, `'Never'`  |
| COMMENT                 | (none)     | Free-text description                                              |

---

## Required Parameters

### `<name>`
Unique identifier for the privacy policy within the schema. Must begin with an alphabetic character. Special characters and spaces require double quotes (identifiers in quotes are case-sensitive).

---

### `AS () RETURNS PRIVACY_BUDGET`
Fixed signature for all privacy policies. The argument list is always empty `()`. The return type is always `PRIVACY_BUDGET`.

---

### `<body>`
SQL expression that evaluates to either `NO_PRIVACY_POLICY()` or a `PRIVACY_BUDGET(...)` call. Determines whether a querying role receives unrestricted access or a differential-privacy budget.

**Simple body (one budget for all roles):**
```sql
-> PRIVACY_BUDGET(BUDGET_NAME => 'default_budget')
```

**Role-based conditional body:**
```sql
-> CASE
     WHEN CURRENT_ROLE() = 'DATA_SCIENTIST'
       THEN PRIVACY_BUDGET(
              BUDGET_NAME => 'ds_budget',
              BUDGET_LIMIT => 100.0,
              MAX_BUDGET_PER_AGGREGATE => 1.0,
              BUDGET_WINDOW => 'Monthly'
            )
     WHEN CURRENT_ROLE() = 'ANALYST'
       THEN PRIVACY_BUDGET(BUDGET_NAME => 'analyst_budget')
     ELSE NO_PRIVACY_POLICY()
   END
```

**Rules:**
- If using a `CASE` expression, an `ELSE` clause is **mandatory** — every possible role/user must receive either a budget or `NO_PRIVACY_POLICY()`.
- Supported context functions: `CURRENT_ROLE()`, `INVOKER_ROLE()`, `CURRENT_USER()`, `CURRENT_ACCOUNT()`.
- Budget names are automatically created by Snowflake the first time they are referenced.

---

## `PRIVACY_BUDGET` Arguments

### `BUDGET_NAME => '<string>'` *(required within PRIVACY_BUDGET)*
Name of the privacy budget. Snowflake automatically provisions this budget object the first time it is referenced.

- For cross-account deployments, namespace the name to avoid collisions:
  ```sql
  BUDGET_NAME => CURRENT_ACCOUNT() || '_ds_budget'
  ```

---

### `BUDGET_LIMIT => <decimal>` *(optional)*
The total amount of privacy loss (epsilon in differential privacy terms) allowed before the budget is exhausted for the current window. Once exhausted, queries against the protected table are blocked until the window resets.

- **Default:** `233.0`
- **Valid values:** Any decimal greater than 0.
- Lower values = stronger privacy protection but queries will hit the limit sooner.

---

### `MAX_BUDGET_PER_AGGREGATE => <decimal>` *(optional)*
The maximum amount of the overall `BUDGET_LIMIT` that a single aggregate query can consume.

- **Default:** `0.5`
- **Valid values:** Any decimal greater than 0; must not exceed `BUDGET_LIMIT`.
- Prevents a single expensive query from exhausting the entire budget.

---

### `BUDGET_WINDOW => '<window>'` *(optional)*
How frequently the privacy budget resets.

| Value      | Reset frequency              |
|------------|------------------------------|
| `'Daily'`  | Every 24 hours               |
| `'Weekly'` | Every 7 days (default)       |
| `'Monthly'`| Every calendar month         |
| `'Yearly'` | Every calendar year          |
| `'Never'`  | Budget never resets (one-time allotment) |

---

## Optional Top-Level Parameters

### `COMMENT = '<string_literal>'`
Free-text description for the privacy policy.

- **Default:** (none)

---

## Access Control Requirements
- `CREATE PRIVACY POLICY` privilege on the schema.
- `APPLY PRIVACY POLICY` privilege to attach the policy to a table.
- Enterprise Edition or higher required.

---

## Constraints & Notes
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Privacy policies control what analysts can **do** with data (aggregation limits), not just what they can **see** — they implement differential privacy.
- A privacy policy is attached to a table; once attached, aggregate queries against the table consume the referenced budget.
- Non-aggregate queries (e.g. `SELECT *`) are blocked entirely for roles subject to a privacy budget.
- Only one privacy policy can be active on a table at a time.
