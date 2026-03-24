# CREATE NETWORK RULE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-network-rule

## Syntax

```sql
CREATE [ OR REPLACE ] NETWORK RULE <name>
   TYPE = { IPV4 | AWSVPCEID | AZURELINKID | GCPPSCID | HOST_PORT | PRIVATE_HOST_PORT }
   VALUE_LIST = ( '<value>' [, '<value>', ... ] )
   MODE = { INGRESS | INTERNAL_STAGE | EGRESS }
   [ COMMENT = '<string_literal>' ]
```

Note: `IF NOT EXISTS` is not supported for NETWORK RULE.

## Defaults Table

| Parameter | Default |
|-----------|---------|
| TYPE | — (required, no default) |
| VALUE_LIST | — (required, no default) |
| MODE | `INGRESS` |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
Identifier for the network rule. Must begin with an alphabetic character and cannot contain spaces or special characters unless enclosed in double quotes.

### `TYPE` (required)
The type of network identifier used in VALUE_LIST. Determines what the rule matches against.

| Value | Description | Compatible MODEs |
|-------|-------------|-----------------|
| `IPV4` | IPv4 addresses or CIDR ranges controlling traffic by origin IP | INGRESS |
| `AWSVPCEID` | AWS VPC endpoint IDs for AWS PrivateLink traffic | INGRESS, INTERNAL_STAGE |
| `AZURELINKID` | Azure Private Endpoint Link IDs | INGRESS |
| `GCPPSCID` | Google Cloud Private Service Connect endpoint connection IDs | INGRESS |
| `HOST_PORT` | Domain names with optional port numbers for outbound traffic | EGRESS |
| `PRIVATE_HOST_PORT` | Single domain with optional port for private outbound connectivity | EGRESS |

### `VALUE_LIST` (required)
One or more values matching the TYPE format.

- **IPV4**: IPv4 addresses or CIDR ranges (e.g., `'192.168.1.0/24'`, `'10.0.0.5'`)
- **AWSVPCEID**: AWS VPC endpoint IDs (e.g., `'vpce-0123456789abcdef0'`)
- **AZURELINKID**: Azure private endpoint resource IDs
- **GCPPSCID**: GCP PSC connection IDs
- **HOST_PORT**: Domain names with optional port (e.g., `'example.com:443'`, `'*.api.example.com'`). Default port is `443`. Wildcard subdomains are supported.
- **PRIVATE_HOST_PORT**: Single domain name with optional port for a private endpoint

### `MODE` (required)
Specifies the direction of network traffic the rule controls.

| Value | Description |
|-------|-------------|
| `INGRESS` | Controls inbound access to the Snowflake service. Default value. |
| `INTERNAL_STAGE` | Restricts access to Snowflake internal stages over AWS PrivateLink (requires TYPE = AWSVPCEID) |
| `EGRESS` | Controls outbound requests from Snowflake (e.g., from UDFs, stored procedures, or external functions) to external services |

### `COMMENT`
A descriptive string for the network rule. Default: none.
