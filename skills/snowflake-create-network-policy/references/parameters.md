# CREATE NETWORK POLICY — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-network-policy

## Syntax

```sql
CREATE [ OR REPLACE ] NETWORK POLICY [ IF NOT EXISTS ] <name>
  [ ALLOWED_NETWORK_RULE_LIST = ( '<network_rule>' [ , '<network_rule>' , ... ] ) ]
  [ BLOCKED_NETWORK_RULE_LIST = ( '<network_rule>' [ , '<network_rule>' , ... ] ) ]
  [ ALLOWED_IP_LIST = ( [ '<ip_address>' ] [ , '<ip_address>' , ... ] ) ]
  [ BLOCKED_IP_LIST = ( [ '<ip_address>' ] [ , '<ip_address>' , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| ALLOWED_NETWORK_RULE_LIST | — (empty, no rules) |
| BLOCKED_NETWORK_RULE_LIST | — (empty, no rules) |
| ALLOWED_IP_LIST | — (none) |
| BLOCKED_IP_LIST | — (none) |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the network policy within the account. Must begin with an alphabetic character; enclose in double quotes if the name contains spaces or special characters. Double-quoted identifiers are case-sensitive.

### `ALLOWED_NETWORK_RULE_LIST`
A list of network rule names (created with `CREATE NETWORK RULE`) that permit access to Snowflake. Supports unlimited entries. References rules by name; the rules must exist in the account.

This is the recommended approach over `ALLOWED_IP_LIST` as network rules support more traffic types (IPv4, AWS PrivateLink, Azure Private Link, GCP PSC).

### `BLOCKED_NETWORK_RULE_LIST`
A list of network rule names that deny access to Snowflake. Blocked rules are evaluated before allowed rules — if an IP/endpoint matches a blocked rule, access is denied regardless of any allowed rule.

### `ALLOWED_IP_LIST`
A legacy parameter listing IPv4 addresses or CIDR ranges that are permitted to access the Snowflake account. Supports up to 100,000 characters total. Examples: `'192.168.1.0/24'`, `'10.0.0.5'`.

Snowflake recommends using network rules (ALLOWED_NETWORK_RULE_LIST) instead.

### `BLOCKED_IP_LIST`
A legacy parameter listing IPv4 addresses or CIDR ranges that are denied access. Evaluated before `ALLOWED_IP_LIST` — an IP appearing in both lists is blocked. Note: `0.0.0.0` is a valid value to block all IPs not in the allowed list.

### `COMMENT`
A descriptive string for the network policy. Default: none.

## Activation

A network policy has no effect until it is attached:
- **Account level**: `ALTER ACCOUNT SET NETWORK_POLICY = <policy_name>`
- **User level**: `ALTER USER <user_name> SET NETWORK_POLICY = <policy_name>`
- **Integration level**: `ALTER INTEGRATION <integration_name> SET NETWORK_POLICY = <policy_name>`
