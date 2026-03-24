# CREATE AUTHENTICATION POLICY — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-authentication-policy

## Syntax

```sql
CREATE [ OR REPLACE ] AUTHENTICATION POLICY [ IF NOT EXISTS ] <name>
  [ AUTHENTICATION_METHODS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
  [ CLIENT_TYPES = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
  [ CLIENT_POLICY = ( <client_type> = ( MINIMUM_VERSION = '<version>' ) [ , ... ] ) ]
  [ SECURITY_INTEGRATIONS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
  [ MFA_ENROLLMENT = { 'REQUIRED' | 'REQUIRED_PASSWORD_ONLY' } ]
  [ MFA_POLICY = ( <list_of_properties> ) ]
  [ PAT_POLICY = ( <list_of_properties> ) ]
  [ WORKLOAD_IDENTITY_POLICY = ( <list_of_properties> ) ]
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| AUTHENTICATION_METHODS | `('ALL')` |
| CLIENT_TYPES | `('ALL')` |
| CLIENT_POLICY | — (no minimum versions enforced) |
| SECURITY_INTEGRATIONS | `('ALL')` |
| MFA_ENROLLMENT | `OPTIONAL` |
| MFA_POLICY.ALLOWED_METHODS | `ALL` |
| MFA_POLICY.ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION | `NONE` |
| PAT_POLICY.DEFAULT_EXPIRY_IN_DAYS | `15` |
| PAT_POLICY.MAX_EXPIRY_IN_DAYS | `365` |
| PAT_POLICY.NETWORK_POLICY_EVALUATION | `ENFORCED_REQUIRED` |
| PAT_POLICY.REQUIRE_ROLE_RESTRICTION_FOR_SERVICE_USERS | `TRUE` |
| WORKLOAD_IDENTITY_POLICY.ALLOWED_PROVIDERS | `ALL` |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
Identifier for the authentication policy. Must start with an alphabetic character and cannot contain spaces or special characters unless enclosed in double quotes. Identifiers in double quotes are case-sensitive.

### `AUTHENTICATION_METHODS`
List of authentication methods allowed during login.

Valid values:
- `'ALL'` — all supported methods (default)
- `'SAML'` — SAML 2.0 via a configured security integration
- `'PASSWORD'` — username and password
- `'OAUTH'` — OAuth2 via a configured security integration
- `'KEYPAIR'` — key-pair (JWT) authentication
- `'PROGRAMMATIC_ACCESS_TOKEN'` — programmatic access tokens (PATs)
- `'WORKLOAD_IDENTITY'` — workload identity federation

### `CLIENT_TYPES`
Clients permitted to authenticate with Snowflake.

Valid values:
- `'ALL'` — all client types (default)
- `'SNOWFLAKE_UI'` — Snowsight web interface
- `'DRIVERS'` — JDBC, ODBC, Python, Go, .NET, etc.
- `'SNOWFLAKE_CLI'` — Snowflake CLI (SnowCLI)
- `'SNOWSQL'` — legacy SnowSQL CLI

### `CLIENT_POLICY`
Sets minimum acceptable client driver versions. Only applicable when CLIENT_TYPES includes `DRIVERS` or `ALL`.

Valid client type keys: `JDBC_DRIVER`, `ODBC_DRIVER`, `PYTHON_DRIVER`, `JAVASCRIPT_DRIVER`, `C_DRIVER`, `GO_DRIVER`, `PHP_DRIVER`, `DOTNET_DRIVER`, `SQL_API`, `SNOWPIPE_STREAMING_CLIENT_SDK`, `PY_CORE`, `SPROC_PYTHON`, `PYTHON_SNOWPARK`, `SQL_ALCHEMY`, `SNOWPARK`, `SNOWFLAKE_CLIENT`

Version format: `'X.X.X'` (e.g., `'3.2.1'`)

### `SECURITY_INTEGRATIONS`
Names of security integrations usable with this policy. Relevant when AUTHENTICATION_METHODS includes `SAML` or `OAUTH`.

Valid values:
- `('ALL')` — any configured security integration (default)
- A quoted list of specific integration names

### `MFA_ENROLLMENT`
Determines whether multi-factor authentication enrollment is required.

Valid values:
- `'REQUIRED'` — all users subject to this policy must enroll in MFA
- `'REQUIRED_PASSWORD_ONLY'` — MFA is required only for password-based logins
- Omitted — defaults to `OPTIONAL` (users may optionally enroll)

### `MFA_POLICY`
Controls MFA enforcement settings. Sub-properties:

- `ALLOWED_METHODS` — MFA method types allowed. Values: `ALL`, `PASSKEY`, `TOTP`, `OTP`, `DUO`. Default: `ALL`.
- `ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION` — Whether to enforce MFA when users authenticate via an external IdP. Values: `ALL`, `NONE`. Default: `NONE`.

### `PAT_POLICY`
Manages programmatic access token (PAT) behavior. Sub-properties:

- `DEFAULT_EXPIRY_IN_DAYS` — Default token lifetime in days. Range: 1–365. Default: `15`.
- `MAX_EXPIRY_IN_DAYS` — Maximum allowed token lifetime. Range: 1–365. Default: `365`.
- `NETWORK_POLICY_EVALUATION` — Whether a network policy is required on the PAT. Values: `ENFORCED_REQUIRED`, `NOT_REQUIRED`. Default: `ENFORCED_REQUIRED`.
- `REQUIRE_ROLE_RESTRICTION_FOR_SERVICE_USERS` — Whether service users' PATs must have a restricted role. Values: `TRUE`, `FALSE`. Default: `TRUE`.

### `WORKLOAD_IDENTITY_POLICY`
Defines workload identity federation constraints. Sub-properties:

- `ALLOWED_PROVIDERS` — Cloud providers allowed for workload identities. Values: `ALL`, `AWS`, `AZURE`, `GCP`, `OIDC`. Default: `ALL`.
- `ALLOWED_AWS_ACCOUNTS` — Specific AWS account IDs permitted (when ALLOWED_PROVIDERS includes `AWS`).
- `ALLOWED_AZURE_ISSUERS` — Azure issuer URLs permitted (when ALLOWED_PROVIDERS includes `AZURE`).
- `ALLOWED_OIDC_ISSUERS` — OIDC issuer URLs permitted (when ALLOWED_PROVIDERS includes `OIDC`).

### `COMMENT`
A descriptive string for the policy. Default: none.
