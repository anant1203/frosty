# CREATE SESSION POLICY — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-session-policy

## Syntax

```sql
CREATE [OR REPLACE] SESSION POLICY [IF NOT EXISTS] <name>
  [ SESSION_IDLE_TIMEOUT_MINS = <integer> ]
  [ SESSION_UI_IDLE_TIMEOUT_MINS = <integer> ]
  [ ALLOWED_SECONDARY_ROLES = ( [ { 'ALL' | <role_name> [ , <role_name> ... ] } ] ) ]
  [ BLOCKED_SECONDARY_ROLES = ( [ { 'ALL' | <role_name> [ , <role_name> ... ] } ] ) ]
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default | Range |
|-----------|---------|-------|
| SESSION_IDLE_TIMEOUT_MINS | `240` (4 hours) | 5–1440 |
| SESSION_UI_IDLE_TIMEOUT_MINS | `240` (4 hours) | 5–1440 |
| ALLOWED_SECONDARY_ROLES | `('ALL')` | — |
| BLOCKED_SECONDARY_ROLES | `()` (none) | — |
| COMMENT | — | — |

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the session policy within the account. Must begin with an alphabetic character; enclose in double quotes if the name contains spaces or special characters.

### `SESSION_IDLE_TIMEOUT_MINS`
The number of minutes of inactivity after which Snowflake clients (drivers, SnowSQL, APIs) require the user to re-authenticate. Applies to all non-UI programmatic clients.

Range: 5–1440 minutes. Default: `240` (4 hours).

### `SESSION_UI_IDLE_TIMEOUT_MINS`
The number of minutes of inactivity in Snowsight (the web UI) after which the user is required to re-authenticate.

Range: 5–1440 minutes. Default: `240` (4 hours).

### `ALLOWED_SECONDARY_ROLES`
Specifies which secondary roles users may activate during a session.

Valid values:
- `('ALL')` — all roles (default)
- `()` — no secondary roles permitted
- `('<role_name>' [, '<role_name>' ...])` — specific named roles only

### `BLOCKED_SECONDARY_ROLES`
Specifies secondary roles that users are explicitly prevented from activating. Takes precedence over `ALLOWED_SECONDARY_ROLES`.

Valid values:
- `()` — no roles blocked (default)
- `('ALL')` — all secondary roles blocked
- `('<role_name>' [, '<role_name>' ...])` — specific named roles blocked

### `COMMENT`
A descriptive string for the session policy. Default: none.

## Activation

The policy has no effect until attached:
- **Account level**: `ALTER ACCOUNT SET SESSION_POLICY = <policy_name>`
- **User level**: `ALTER USER <user_name> SET SESSION_POLICY = <policy_name>`
