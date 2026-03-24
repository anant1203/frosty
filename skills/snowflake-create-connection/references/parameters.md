# Snowflake CREATE CONNECTION — Parameter Reference

## Syntax Variants

### Primary Connection (new connection in source account)

```sql
CREATE CONNECTION [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
```

### Secondary Connection (replica of an existing primary connection)

```sql
CREATE CONNECTION [ IF NOT EXISTS ] <name>
  AS REPLICA OF <organization_name>.<account_name>.<name>
  [ COMMENT = '<string_literal>' ]
```

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| AS REPLICA OF | (none) | Omit for primary connections; required for secondary |
| COMMENT | (none) | Free-text description |

---

## Required Parameters

### name
- Unique identifier for the connection
- Must start with an alphabetic character
- May only contain letters, digits (0–9), and underscores (_)
- For **primary connections**: must be unique across all connection names and account names within the organization
- For **secondary connections**: must exactly match the primary connection's name

---

## Optional Parameters (Primary Connection)

### COMMENT = '<string_literal>'
- Free-text description of the connection
- Displayed in `SHOW CONNECTIONS` output
- Default: no value

---

## Secondary Connection Parameters

### AS REPLICA OF <organization_name>.<account_name>.<name>
- Designates this connection as a replica of an existing primary connection
- `organization_name`: Snowflake organization identifier
- `account_name`: account identifier where the primary connection resides
- `name`: identifier of the primary connection to replicate
- The secondary connection name must match `<name>` exactly

### COMMENT = '<string_literal>'
- Same as for primary connections; can be set independently on the secondary
- Default: no value

---

## Primary vs. Secondary Connection

| Aspect | Primary Connection | Secondary Connection |
|---|---|---|
| Syntax | `CREATE CONNECTION IF NOT EXISTS <name>` | `CREATE CONNECTION IF NOT EXISTS <name> AS REPLICA OF ...` |
| Name uniqueness | Must be unique across org-level connection and account names | Must match the primary connection name exactly |
| Purpose | Entry point for client connection URL | Standby endpoint for failover / disaster recovery |
| Account | Source account | Target account |

---

## Access Control Requirements
- Only users with the **ACCOUNTADMIN** role can execute `CREATE CONNECTION`
- No additional object-level privileges are required
