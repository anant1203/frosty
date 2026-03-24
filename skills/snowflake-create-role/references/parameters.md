# CREATE ROLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-role

## Full Syntax

```sql
CREATE [ OR REPLACE ] ROLE [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

## Variant: CREATE OR ALTER ROLE (Preview Feature)

```sql
CREATE OR ALTER ROLE <name>
  [ COMMENT = '<string_literal>' ]
```

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the role within the account. Must start with an alphabetic character. Cannot contain spaces or special characters unless enclosed in double quotes. Double-quoted identifiers are case-sensitive. |

## Optional Parameters Defaults Table

| Parameter | Default |
|-----------|---------|
| `COMMENT` | No value (NULL) |
| `TAG` | None assigned |

## Optional Parameters — Detailed Descriptions

**`COMMENT = '<string_literal>'`**
A free-text description of the role's purpose, intended privilege scope, or owning team. Strongly recommended for governance and auditability. Default: no value.

**`TAG ( <tag_name> = '<tag_value>' [ , ... ] )`**
Assigns one or more object tag name-value pairs to the role. Tag values are always strings with a maximum of 256 characters. Multiple tags are comma-separated. Tags on a role are not inherited by objects the role has privileges on.

## Behavioral Notes

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive and cannot both appear in the same statement.
- `CREATE OR REPLACE ROLE` is atomic: the old role is dropped and the new one is created in a single transaction. All existing privilege grants on the replaced role are lost.
- For `CREATE OR ALTER ROLE`: existing tag assignments remain unchanged; modifying tags via this form is not supported.
- After creation the role must be explicitly granted to users or to other roles via `GRANT ROLE <name> TO USER/ROLE` before it has any effect.
- The creator of a role is automatically granted the OWNERSHIP privilege on it, which can be transferred via `GRANT OWNERSHIP`.
- Avoid storing personal, sensitive, or regulated data in the role name or comment field (Snowflake metadata restriction).

## Access Control Requirements

| Privilege | Object | Notes |
|-----------|--------|-------|
| CREATE ROLE | Account | Required to create a new role. By default only USERADMIN or higher has this; it can be granted to other roles. |
| OWNERSHIP | Role | Required to run CREATE OR ALTER ROLE on an existing role. |
