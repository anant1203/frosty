# Snowflake CREATE FAILOVER GROUP — Parameter Reference

## Syntax Variants

### Primary Failover Group (source account)

```sql
CREATE FAILOVER GROUP [ IF NOT EXISTS ] <name>
    OBJECT_TYPES = <object_type> [ , <object_type> , ... ]
    [ ALLOWED_DATABASES = <db_name> [ , <db_name> , ... ] ]
    [ ALLOWED_EXTERNAL_VOLUMES = <external_volume_name> [ , <external_volume_name> , ... ] ]
    [ ALLOWED_SHARES = <share_name> [ , <share_name> , ... ] ]
    [ ALLOWED_INTEGRATION_TYPES = <integration_type_name> [ , <integration_type_name> , ... ] ]
    ALLOWED_ACCOUNTS = <org_name>.<target_account_name> [ , <org_name>.<target_account_name> , ... ]
    [ IGNORE EDITION CHECK ]
    [ REPLICATION_SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }' ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ ERROR_INTEGRATION = <integration_name> ]
```

### Secondary Failover Group (target account)

```sql
CREATE FAILOVER GROUP [ IF NOT EXISTS ] <secondary_name>
    AS REPLICA OF <org_name>.<source_account_name>.<name>
```

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| OBJECT_TYPES | (required) | Must list all object categories to replicate |
| ALLOWED_DATABASES | (none) | Required when DATABASES is in OBJECT_TYPES |
| ALLOWED_EXTERNAL_VOLUMES | (none) | Required when EXTERNAL VOLUMES is in OBJECT_TYPES |
| ALLOWED_SHARES | (none) | Required when SHARES is in OBJECT_TYPES |
| ALLOWED_INTEGRATION_TYPES | (none) | Required when INTEGRATIONS is in OBJECT_TYPES |
| ALLOWED_ACCOUNTS | (required) | org_name.account_name format |
| IGNORE EDITION CHECK | false | Omit unless replicating to lower editions |
| REPLICATION_SCHEDULE | (none) | No automatic schedule; refresh must be triggered manually |
| TAG | (none) | Metadata tags |
| ERROR_INTEGRATION | (none) | No error notification by default |

---

## Required Parameters

### name
- Identifier for the failover group
- Must begin with an alphabetic character
- Case-sensitive if quoted

### OBJECT_TYPES = <object_type> [ , <object_type> , ... ]
- Specifies which categories of objects to include in the failover group
- Valid values:
  - `ACCOUNT PARAMETERS`
  - `DATABASES`
  - `EXTERNAL VOLUMES`
  - `INTEGRATIONS`
  - `LISTINGS`
  - `NETWORK POLICIES`
  - `PROFILES`
  - `RESOURCE MONITORS`
  - `ROLES`
  - `SHARES`
  - `USERS`
  - `WAREHOUSES`

### ALLOWED_ACCOUNTS = <org_name>.<target_account_name> [ , ... ]
- One or more target accounts that may create secondary replicas of this failover group
- Format: `<organization_name>.<account_name>`
- Required for primary failover groups

---

## Conditional Required Parameters

### ALLOWED_DATABASES = <db_name> [ , ... ]
- Required when `DATABASES` is included in `OBJECT_TYPES`
- Lists the specific databases to include in replication

### ALLOWED_EXTERNAL_VOLUMES = <external_volume_name> [ , ... ]
- Required when `EXTERNAL VOLUMES` is included in `OBJECT_TYPES`
- Lists the specific external volumes to include

### ALLOWED_SHARES = <share_name> [ , ... ]
- Required when `SHARES` is included in `OBJECT_TYPES`
- Lists the specific shares to include

### ALLOWED_INTEGRATION_TYPES = <integration_type_name> [ , ... ]
- Required when `INTEGRATIONS` is included in `OBJECT_TYPES`
- Valid values:
  - `SECURITY INTEGRATIONS`
  - `API INTEGRATIONS`
  - `STORAGE INTEGRATIONS`
  - `EXTERNAL ACCESS INTEGRATIONS`
  - `NOTIFICATION INTEGRATIONS`

---

## Optional Parameters

### IGNORE EDITION CHECK
- Allows replication to target accounts that do not have a matching Business Critical Edition agreement
- Use with caution: the target account may not support all features being replicated
- Omit unless explicitly needed

### REPLICATION_SCHEDULE = '{ <num> MINUTE | USING CRON <expr> <time_zone> }'
- Sets an automatic refresh schedule for secondary failover groups
- Options:
  - `'<num> MINUTE'` — interval in minutes; maximum is 11520 minutes (8 days)
  - `'USING CRON <expr> <time_zone>'` — standard cron expression with a time zone (e.g., `'USING CRON 0 */6 * * * America/New_York'`)
- Default: none (manual refresh required)

### TAG ( <tag_name> = '<tag_value>' [ , ... ] )
- Assigns metadata tags to the failover group
- Tag values are limited to 256 characters each
- Default: none

### ERROR_INTEGRATION = <integration_name>
- Name of a notification integration that receives alerts when a scheduled refresh fails
- Default: none

---

## Secondary Failover Group Parameters

### AS REPLICA OF <org_name>.<source_account_name>.<name>
- Identifies the primary failover group to replicate from
- `org_name`: the Snowflake organization name
- `source_account_name`: the account containing the primary group
- `name`: the primary failover group name
- The secondary group name must match the primary group name

---

## Access Control Requirements
- Must have ACCOUNTADMIN role or equivalent privilege to create failover groups
- Business Critical Edition (or higher) is required for this feature
- Target accounts listed in ALLOWED_ACCOUNTS must also have Business Critical Edition (unless IGNORE EDITION CHECK is used)
