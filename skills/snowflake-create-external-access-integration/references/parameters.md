# CREATE EXTERNAL ACCESS INTEGRATION — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration

## Syntax

```sql
CREATE [ OR REPLACE ] EXTERNAL ACCESS INTEGRATION <name>
  ALLOWED_NETWORK_RULES = ( <rule_name_1> [, <rule_name_2>, ... ] )
  [ ALLOWED_API_AUTHENTICATION_INTEGRATIONS = { ( <integration_name_1> [, <integration_name_2>, ... ] ) | none } ]
  [ ALLOWED_AUTHENTICATION_SECRETS = { ( <secret_name_1> [, <secret_name_2>, ... ] ) | all | none } ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

Note: `IF NOT EXISTS` is not supported for EXTERNAL ACCESS INTEGRATION.

## Defaults Table

| Parameter | Default |
|-----------|---------|
| ALLOWED_NETWORK_RULES | — (required, no default) |
| ALLOWED_API_AUTHENTICATION_INTEGRATIONS | — (not set) |
| ALLOWED_AUTHENTICATION_SECRETS | `none` |
| ENABLED | `TRUE` |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
Identifier for the external access integration. Must start with an alphabetic character; enclose in double quotes if the name contains special characters.

### `ALLOWED_NETWORK_RULES` (required)
A list of network rule object names that define which external network locations Snowflake may access. Only EGRESS-mode network rules are permitted here; specifying INGRESS or INTERNAL_STAGE rules will cause an error.

Format: `( rule_name_1 [, rule_name_2, ...] )`

### `ALLOWED_API_AUTHENTICATION_INTEGRATIONS`
A list of security integrations (TYPE = API_AUTHENTICATION) that provide OAuth credentials for the external service. Only relevant when the external endpoint requires OAuth2 authorization.

Valid values:
- `( integration_name_1 [, integration_name_2, ...] )` — specific named integrations
- `none` — no API authentication integrations allowed (default behavior)

### `ALLOWED_AUTHENTICATION_SECRETS`
Specifies which SECRET objects may be used by handler code when accessing external locations through this integration.

Valid values:
- `( secret_name_1 [, secret_name_2, ...] )` — explicit list of secret object names
- `all` — all secrets in the account
- `none` — no secrets allowed (default)

Prefer listing specific secrets over `all` to follow least-privilege principles.

### `ENABLED` (required)
Controls whether the integration is active and usable by handler code.

Valid values:
- `TRUE` — integration is active (default)
- `FALSE` — integration is suspended

### `COMMENT`
A descriptive string for the integration. Default: none.

## Access Control Prerequisites

- The role creating the integration must have the `CREATE INTEGRATION` privilege on the account.
- The handler code (UDF or stored procedure) must reference this integration via `EXTERNAL_ACCESS_INTEGRATIONS = ( <name> )` in its DDL.
