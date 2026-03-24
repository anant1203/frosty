# Snowflake CREATE TAG — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] TAG [ IF NOT EXISTS ] <name>
    [ ALLOWED_VALUES '<val_1>' [ , '<val_2>' [ , ... ] ] ]
    [ PROPAGATE = { ON_DEPENDENCY_AND_DATA_MOVEMENT | ON_DEPENDENCY | ON_DATA_MOVEMENT }
      [ ON_CONFLICT = { '<string>' | ALLOWED_VALUES_SEQUENCE } ] ]
    [ COMMENT = '<string_literal>' ]
```

---

## Parameter Defaults

| Parameter       | Default                         | Notes                                                    |
|-----------------|---------------------------------|----------------------------------------------------------|
| ALLOWED_VALUES  | NULL (all string values allowed) | Max 5,000 values; must be listed before other parameters |
| PROPAGATE       | (none / disabled)               | Enterprise Edition only                                  |
| ON_CONFLICT     | `'CONFLICT'` (literal string)   | Only relevant when PROPAGATE is set                      |
| COMMENT         | (none)                          | Free-text description                                    |

---

## Required Parameters

### `<name>`
Identifier for the tag. Must begin with an alphabetic character. Cannot contain spaces or special characters unless enclosed in double quotes (double-quoted identifiers are case-sensitive).

---

## Optional Parameters

### `ALLOWED_VALUES '<val_1>' [ , '<val_2>' [ , ... ] ]`
Restricts the tag to a predefined list of string values. When set, any attempt to assign the tag a value not in this list will fail.

- **Default:** NULL — all string values are permitted.
- **Limit:** Maximum 5,000 values per tag.
- **Ordering:** Must appear before `PROPAGATE` and `COMMENT` in the statement.
- **Use when:** The user wants controlled vocabulary (e.g. environment tags: `'prod'`, `'dev'`, `'staging'`).

```sql
CREATE TAG IF NOT EXISTS env
    ALLOWED_VALUES 'prod', 'dev', 'staging';
```

---

### `PROPAGATE = { ON_DEPENDENCY_AND_DATA_MOVEMENT | ON_DEPENDENCY | ON_DATA_MOVEMENT }`
*(Enterprise Edition only)* Enables automatic propagation of the tag to downstream objects.

| Value                           | Behaviour                                                   |
|---------------------------------|-------------------------------------------------------------|
| `ON_DEPENDENCY_AND_DATA_MOVEMENT` | Propagates on both object dependencies and data movement  |
| `ON_DEPENDENCY`                 | Propagates only when object dependencies are resolved       |
| `ON_DATA_MOVEMENT`              | Propagates only when data moves between objects             |

- **Default:** Not set (propagation disabled).
- **Use when:** Customers need automatic lineage-based tag inheritance.

---

### `ON_CONFLICT = { '<string>' | ALLOWED_VALUES_SEQUENCE }`
*(Enterprise Edition only)* Determines the tag value used when a propagation conflict occurs (i.e. two different values would be assigned to the same object).

| Value                    | Behaviour                                                                              |
|--------------------------|----------------------------------------------------------------------------------------|
| `'<string>'`             | A literal string that becomes the tag value on conflict                                |
| `ALLOWED_VALUES_SEQUENCE` | Uses the first value in the `ALLOWED_VALUES` list that resolves the conflict          |

- **Default:** `'CONFLICT'` (the literal string is written as the tag value when a conflict is detected).
- **Requires:** `PROPAGATE` to be set; has no effect without it.

---

### `COMMENT = '<string_literal>'`
Free-text description for the tag visible in Snowsight and `SHOW TAGS`.

- **Default:** (none)
- Do not store sensitive, regulated, or personal data in this field.

---

## Access Control Requirements
- `CREATE TAG` privilege on the schema (granted to SYSADMIN by default when using standard role hierarchy).
- Enterprise Edition or higher is required for `PROPAGATE` and `ON_CONFLICT`.

---

## Constraints & Notes
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Tag identifiers, allowed values, and comments are metadata fields — do not populate them with sensitive or regulated data.
- Tags can be assigned to most Snowflake objects via `CREATE … TAG (…)` or `ALTER … SET TAG (…)`.
