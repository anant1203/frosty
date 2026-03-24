# CREATE SECRET — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-secret

## Syntax Variants

### TYPE = GENERIC_STRING
```sql
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = GENERIC_STRING
  SECRET_STRING = '<string_literal>'
  [ COMMENT = '<string_literal>' ]
```

### TYPE = PASSWORD
```sql
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = PASSWORD
  USERNAME = '<username>'
  PASSWORD = '<password>'
  [ COMMENT = '<string_literal>' ]
```

### TYPE = OAUTH2 (Client Credentials Flow)
```sql
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = OAUTH2
  API_AUTHENTICATION = <security_integration_name>
  OAUTH_SCOPES = ( '<scope_1>' [ , '<scope_2>' ... ] )
  [ COMMENT = '<string_literal>' ]
```

### TYPE = OAUTH2 (Authorization Code Grant Flow)
```sql
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = OAUTH2
  OAUTH_REFRESH_TOKEN = '<string_literal>'
  OAUTH_REFRESH_TOKEN_EXPIRY_TIME = '<string_literal>'
  API_AUTHENTICATION = <security_integration_name>
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| TYPE | — (required) |
| SECRET_STRING | — (required for GENERIC_STRING) |
| USERNAME | — (required for PASSWORD) |
| PASSWORD | — (required for PASSWORD) |
| API_AUTHENTICATION | — (required for OAUTH2) |
| OAUTH_SCOPES | All scopes defined in the referenced security integration |
| OAUTH_REFRESH_TOKEN | — (required for OAUTH2 auth-code grant) |
| OAUTH_REFRESH_TOKEN_EXPIRY_TIME | — (required for OAUTH2 auth-code grant) |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the secret within the schema. Must start with an alphabetic character; enclose in double quotes if the name contains special characters.

### `TYPE` (required)
Determines the category and structure of the secret.

| Value | Use Case |
|-------|----------|
| `GENERIC_STRING` | Arbitrary sensitive strings — API tokens, SSH keys, connection strings |
| `PASSWORD` | Username + password pairs for basic authentication |
| `OAUTH2` | OAuth2 credentials — either client-credentials flow or authorization-code-grant flow |

### `SECRET_STRING` (required for GENERIC_STRING)
The sensitive string value to store in the secret. This value is encrypted at rest and is never displayed after creation. Examples: API keys, bearer tokens, connection strings.

### `USERNAME` (required for PASSWORD)
The username value to store in the secret. Stored encrypted at rest.

### `PASSWORD` (required for PASSWORD)
The password value to store in the secret. Stored encrypted at rest and never displayed after creation.

### `API_AUTHENTICATION` (required for OAUTH2)
The name of the Snowflake security integration of TYPE = API_AUTHENTICATION that defines the OAuth2 server and client credentials. The integration must exist before creating the secret.

### `OAUTH_SCOPES` (optional for OAUTH2 client-credentials flow)
A comma-separated list of OAuth scopes to request when obtaining access tokens. Each scope must be a subset of the `OAUTH_ALLOWED_SCOPES` defined in the referenced security integration.

Default: all scopes defined in the security integration's `OAUTH_ALLOWED_SCOPES`.

### `OAUTH_REFRESH_TOKEN` (required for OAUTH2 authorization-code-grant flow)
The OAuth refresh token obtained from the authorization server. Used to obtain new access tokens when the current one expires. Stored encrypted at rest.

### `OAUTH_REFRESH_TOKEN_EXPIRY_TIME` (required for OAUTH2 authorization-code-grant flow)
The timestamp when the refresh token expires. Provided as a string in timestamp format (e.g., `'2025-12-31 00:00:00'`). Snowflake uses this value to determine when the secret needs to be updated.

### `COMMENT`
A descriptive string for the secret. Default: none.

## Security Notes

- Secret values (SECRET_STRING, PASSWORD, OAUTH_REFRESH_TOKEN) are encrypted at rest and are never returned in plain text after creation.
- Access to secrets requires the `READ` privilege on the secret object.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
