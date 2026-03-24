# CREATE USER — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-user

## Full Syntax

```sql
CREATE [ OR REPLACE ] USER [ IF NOT EXISTS ] <name>
  [ objectProperties ]
  [ objectParams ]
  [ sessionParams ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the user within the account. Must start with an alphabetic character. Special characters require double-quoting. Note: this is NOT the login name — users log in with `LOGIN_NAME`. |

## Object Properties Defaults Table

| Parameter | Default |
|-----------|---------|
| `PASSWORD` | NULL (no password; user cannot log in until set) |
| `LOGIN_NAME` | Same as `<name>` |
| `DISPLAY_NAME` | Same as `<name>` |
| `FIRST_NAME` | NULL |
| `MIDDLE_NAME` | NULL |
| `LAST_NAME` | NULL |
| `EMAIL` | NULL |
| `MUST_CHANGE_PASSWORD` | FALSE |
| `DISABLED` | FALSE |
| `ALLOWED_INTERFACES` | ('ALL') |
| `DAYS_TO_EXPIRY` | NULL (no expiry) |
| `MINS_TO_UNLOCK` | NULL |
| `DEFAULT_WAREHOUSE` | NULL |
| `DEFAULT_NAMESPACE` | NULL |
| `DEFAULT_ROLE` | NULL |
| `DEFAULT_SECONDARY_ROLES` | ('ALL') |
| `MINS_TO_BYPASS_MFA` | NULL |
| `RSA_PUBLIC_KEY` | NULL |
| `RSA_PUBLIC_KEY_FP` | NULL |
| `RSA_PUBLIC_KEY_2` | NULL |
| `RSA_PUBLIC_KEY_2_FP` | NULL |
| `TYPE` | PERSON |
| `WORKLOAD_IDENTITY` | NULL |
| `COMMENT` | NULL |

## Object Properties — Detailed Descriptions

**`PASSWORD = '<string>'`**
The user's login password. Must be a quoted string. If omitted at creation time the user cannot log in until a password is set via ALTER USER. Not applicable for TYPE = SERVICE users (use RSA_PUBLIC_KEY instead).

**`LOGIN_NAME = <string>`**
The name the user types at the Snowflake login prompt. Case-insensitive. May include spaces and special characters if quoted. Defaults to the user's `<name>` identifier.

**`DISPLAY_NAME = <string>`**
The name shown in the Snowflake web interface. Defaults to the user's `<name>` identifier.

**`FIRST_NAME / MIDDLE_NAME / LAST_NAME = <string>`**
Human name components. Informational only.

**`EMAIL = <string>`**
User's email address. Required for Snowflake Community access and for receiving resource monitor notifications.

**`MUST_CHANGE_PASSWORD = TRUE | FALSE`**
When TRUE, forces the user to change their password on the very next login. Recommended for new human users who receive an initial temporary password. Default: FALSE.

**`DISABLED = TRUE | FALSE`**
When TRUE, the user cannot log in. For an already-connected session, running queries are aborted immediately. Default: FALSE.

**`ALLOWED_INTERFACES = ('ALL' | '<interface>' [, ...])`**
Controls which Snowflake interfaces the user may access. Valid interface values: SNOWFLAKE_INTELLIGENCE, STREAMLIT. Default: ('ALL').

**`DAYS_TO_EXPIRY = <integer>`**
Number of days until the user account automatically expires. Cannot be applied to ACCOUNTADMIN users. Default: NULL (never expires).

**`MINS_TO_UNLOCK = <integer>`**
Number of minutes until a temporary login lock (caused by repeated failed login attempts) is automatically cleared. Setting to 0 unlocks immediately. Default: NULL.

**`DEFAULT_WAREHOUSE = <string>`**
The virtual warehouse set as active when the user logs in. The user must have USAGE privilege on this warehouse. Default: NULL.

**`DEFAULT_NAMESPACE = <string>`**
The default database or fully-qualified schema (`db.schema`) active at login. Default: NULL.

**`DEFAULT_ROLE = <string>`**
The role activated by default at login. Must be explicitly granted to the user separately. Default: NULL.

**`DEFAULT_SECONDARY_ROLES = ('ALL') | ()`**
Secondary roles active at login. ('ALL') activates all roles granted to the user. () disables secondary roles. Default: ('ALL').

**`MINS_TO_BYPASS_MFA = <integer>`**
Temporarily bypasses MFA for the specified number of minutes. Default: NULL.

**`RSA_PUBLIC_KEY = <string>`**
The user's RSA public key for key-pair authentication (replaces password for service accounts). Default: NULL.

**`RSA_PUBLIC_KEY_FP = <string>`**
Fingerprint of the RSA public key. Read-only; set automatically by Snowflake. Default: NULL.

**`RSA_PUBLIC_KEY_2 / RSA_PUBLIC_KEY_2_FP`**
Secondary RSA key pair used for zero-downtime key rotation. Default: NULL.

**`TYPE = PERSON | SERVICE | LEGACY_SERVICE`**
Classifies the user.
- PERSON: A human user (default).
- SERVICE: A non-human application/service account. Cannot have a password; must use key-pair or OAuth authentication.
- LEGACY_SERVICE: Deprecated predecessor to SERVICE; included for backward compatibility.

**`WORKLOAD_IDENTITY = ( <properties> )`**
Federation configuration for workload identity. Requires `TYPE` specifying the cloud provider (AWS, AZURE, GCP, or OIDC) along with provider-specific fields (ARN, ISSUER, SUBJECT). Default: NULL.

**`COMMENT = '<string>'`**
Free-text description of the user. Default: NULL.

## Object Parameters Defaults Table

| Parameter | Default |
|-----------|---------|
| `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR` | FALSE |
| `ENABLE_UNREDACTED_SECURE_OBJECT_ERROR` | FALSE |
| `NETWORK_POLICY` | NULL (account-level policy applies) |

## Object Parameters — Detailed Descriptions

**`ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR = TRUE | FALSE`**
Controls whether query syntax error messages show the full SQL text or a redacted version. Default: FALSE (redacted).

**`ENABLE_UNREDACTED_SECURE_OBJECT_ERROR = TRUE | FALSE`**
Controls whether error messages involving secure objects include metadata that would otherwise be redacted. Default: FALSE.

**`NETWORK_POLICY = <string>`**
Assigns a named network policy to the user, restricting the IP addresses from which they may connect. Overrides any account-level network policy for this user.

## Session Parameters (Selected Common Values)

Session parameters override account-level defaults for this specific user's sessions. Common parameters include:

| Parameter | Description | Typical Default |
|-----------|-------------|-----------------|
| `TIMEZONE` | Session timezone (e.g., `'America/Los_Angeles'`) | Account-level setting |
| `DATE_OUTPUT_FORMAT` | Format for DATE display (e.g., `'YYYY-MM-DD'`) | Account-level setting |
| `TIME_OUTPUT_FORMAT` | Format for TIME display | Account-level setting |
| `TIMESTAMP_OUTPUT_FORMAT` | Format for TIMESTAMP display | Account-level setting |
| `AUTOCOMMIT` | Whether DML auto-commits (TRUE/FALSE) | TRUE |
| `STATEMENT_TIMEOUT_IN_SECONDS` | Max execution time before cancellation | Account-level setting |
| `QUERY_TAG` | Default tag attached to all queries | NULL |

Full session parameter list: https://docs.snowflake.com/en/sql-reference/parameters

## Tags

```sql
[ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] )
```

Tag values are strings; maximum 256 characters per value.

## Access Control Requirements

The `CREATE USER` privilege on the account is required. By default only the USERADMIN role (and higher) has this privilege.
