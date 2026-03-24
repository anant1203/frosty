# CREATE PASSWORD POLICY — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-password-policy

## Syntax

```sql
CREATE [ OR REPLACE ] PASSWORD POLICY [ IF NOT EXISTS ] <name>
  [ PASSWORD_MIN_LENGTH = <integer> ]
  [ PASSWORD_MAX_LENGTH = <integer> ]
  [ PASSWORD_MIN_UPPER_CASE_CHARS = <integer> ]
  [ PASSWORD_MIN_LOWER_CASE_CHARS = <integer> ]
  [ PASSWORD_MIN_NUMERIC_CHARS = <integer> ]
  [ PASSWORD_MIN_SPECIAL_CHARS = <integer> ]
  [ PASSWORD_MIN_AGE_DAYS = <integer> ]
  [ PASSWORD_MAX_AGE_DAYS = <integer> ]
  [ PASSWORD_MAX_RETRIES = <integer> ]
  [ PASSWORD_LOCKOUT_TIME_MINS = <integer> ]
  [ PASSWORD_HISTORY = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default | Range |
|-----------|---------|-------|
| PASSWORD_MIN_LENGTH | `14` | 8–256 |
| PASSWORD_MAX_LENGTH | `256` | 8–256 |
| PASSWORD_MIN_UPPER_CASE_CHARS | `1` | 0–256 |
| PASSWORD_MIN_LOWER_CASE_CHARS | `1` | 0–256 |
| PASSWORD_MIN_NUMERIC_CHARS | `1` | 0–256 |
| PASSWORD_MIN_SPECIAL_CHARS | `0` | 0–256 |
| PASSWORD_MIN_AGE_DAYS | `0` | 0–999 |
| PASSWORD_MAX_AGE_DAYS | `90` | 0–999 |
| PASSWORD_MAX_RETRIES | `5` | 1–10 |
| PASSWORD_LOCKOUT_TIME_MINS | `15` | 1–999 |
| PASSWORD_HISTORY | `5` | 1–24 |
| COMMENT | — | — |

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the password policy within your account. Must begin with an alphabetic character; enclose in double quotes if the name contains special characters. Double-quoted identifiers are case-sensitive.

### `PASSWORD_MIN_LENGTH`
Specifies the minimum number of characters the password must contain. Must be less than or equal to `PASSWORD_MAX_LENGTH`. Range: 8–256. Default: `14`.

### `PASSWORD_MAX_LENGTH`
Specifies the maximum number of characters the password can contain. Must be greater than or equal to `PASSWORD_MIN_LENGTH`. Range: 8–256. Default: `256`.

### `PASSWORD_MIN_UPPER_CASE_CHARS`
Minimum number of uppercase (A–Z) characters required in the password. Range: 0–256. Default: `1`.

### `PASSWORD_MIN_LOWER_CASE_CHARS`
Minimum number of lowercase (a–z) characters required in the password. Range: 0–256. Default: `1`.

### `PASSWORD_MIN_NUMERIC_CHARS`
Minimum number of numeric (0–9) characters required in the password. Range: 0–256. Default: `1`.

### `PASSWORD_MIN_SPECIAL_CHARS`
Minimum number of special characters (e.g., `!`, `@`, `#`) required in the password. Range: 0–256. Default: `0`.

### `PASSWORD_MIN_AGE_DAYS`
Number of days a user must wait before they can change their password again. Range: 0–999. Default: `0` (no minimum age enforced).

### `PASSWORD_MAX_AGE_DAYS`
Maximum number of days before the user is required to change their password. Set to `0` to disable password expiration. Range: 0–999. Default: `90`.

### `PASSWORD_MAX_RETRIES`
Maximum number of consecutive failed login attempts before the account is locked. Range: 1–10. Default: `5`.

### `PASSWORD_LOCKOUT_TIME_MINS`
Number of minutes the account remains locked after exceeding `PASSWORD_MAX_RETRIES`. Range: 1–999. Default: `15`.

### `PASSWORD_HISTORY`
Number of most-recent passwords stored to prevent reuse. Users cannot reuse any of the last N passwords. Range: 1–24. Default: `5`.

Note: This check only applies to passwords changed after the policy is attached; it does not retroactively evaluate existing password history.

### `COMMENT`
A descriptive string for the policy. Default: none.
