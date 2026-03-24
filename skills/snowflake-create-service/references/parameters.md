# Snowflake CREATE SERVICE — Parameter Reference

## Syntax

```sql
CREATE SERVICE [ IF NOT EXISTS ] <name>
  IN COMPUTE POOL <compute_pool_name>
  {
     fromSpecification
     | fromSpecificationTemplate
  }
  [ AUTO_SUSPEND_SECS = <num> ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <EAI_name> [ , ... ] ) ]
  [ AUTO_RESUME = { TRUE | FALSE } ]
  [ MIN_INSTANCES = <num> ]
  [ MIN_READY_INSTANCES = <num> ]
  [ MAX_INSTANCES = <num> ]
  [ LOG_LEVEL = '<log_level>' ]
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

### fromSpecification variants

```sql
-- Inline specification
FROM SPECIFICATION <specification_text>

-- From a stage file
FROM @<stage> SPECIFICATION_FILE = '<yaml_file_path>'

-- From a file relative to the Native App root directory
FROM SPECIFICATION_FILE = '<yaml_file_path>'
```

### fromSpecificationTemplate variants

```sql
-- Inline specification template
FROM SPECIFICATION_TEMPLATE <specification_text>
  USING ( <key> => <value> [ , <key> => <value> [ , ... ] ] )

-- From a stage file template
FROM @<stage> SPECIFICATION_TEMPLATE_FILE = '<yaml_file_path>'
  USING ( <key> => <value> [ , ... ] )

-- From a file relative to the Native App root directory
FROM SPECIFICATION_TEMPLATE_FILE = '<yaml_file_path>'
  USING ( <key> => <value> [ , ... ] )
```

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| AUTO_SUSPEND_SECS | 0 (disabled) | Minimum effective value is 300 seconds |
| AUTO_RESUME | TRUE | Service resumes automatically when called |
| MIN_INSTANCES | 1 | Minimum running instances |
| MIN_READY_INSTANCES | Value of MIN_INSTANCES | Must be ≤ MIN_INSTANCES |
| MAX_INSTANCES | Value of MIN_INSTANCES | Set higher for horizontal scaling |
| LOG_LEVEL | (none) | Platform event logging severity |
| QUERY_WAREHOUSE | (none) | Warehouse for container SQL queries |
| EXTERNAL_ACCESS_INTEGRATIONS | (none) | External network access |
| TAG | (none) | Metadata tags |
| COMMENT | (none) | Free-text description |

---

## Required Parameters

### name
- Unique identifier for the service within the schema
- Must start with an alphabetic character
- Quoted names (for special characters or case-sensitivity) are not supported
- The same no-quote constraint applies to the containing database and schema names

### IN COMPUTE POOL <compute_pool_name>
- Designates the compute pool where service containers will run
- The compute pool must exist and be in ACTIVE or IDLE state
- The user must have USAGE privilege on the compute pool

### FROM ... (specification source)
- Exactly one specification source must be provided
- Inline `FROM SPECIFICATION <text>`: embed the YAML service specification directly in the DDL
- `FROM @<stage> SPECIFICATION_FILE = '<path>'`: reference a YAML file on a Snowflake stage
- `FROM SPECIFICATION_FILE = '<path>'`: reference a file in the Native App root (for Snowflake Native Apps)
- Template variants (`FROM SPECIFICATION_TEMPLATE ...`) require a `USING` clause to supply variable values

### USING ( <key> => <value> [ , ... ] ) — Required with template variants
- Provides values for variables defined in the specification template
- Keys and values may be alphanumeric identifiers or valid JSON values
- String values must be enclosed in single quotes or `$$..$$`

---

## Optional Parameters

### AUTO_SUSPEND_SECS = <num>
- Number of seconds of inactivity after which Snowflake automatically suspends the service
- `0` (default): auto-suspension is disabled
- Minimum effective value: `300` seconds; values between 1 and 299 are accepted but treated as disabled
- Set to a non-zero value to reduce compute costs for intermittently used services

### EXTERNAL_ACCESS_INTEGRATIONS = ( <EAI_name> [ , ... ] )
- List of External Access Integration names that allow service containers to make outbound network calls
- Names are case-sensitive
- Requires CREATE EXTERNAL ACCESS INTEGRATION privilege
- Default: none (no external network access)

### AUTO_RESUME = { TRUE | FALSE }
- `TRUE` (default): the service automatically resumes from suspended state when invoked via a service function or public ingress endpoint
- `FALSE`: the service must be manually resumed with `ALTER SERVICE ... RESUME`

### MIN_INSTANCES = <num>
- Minimum number of service instances that must be running at all times
- Default: `1`
- Increasing this value ensures a baseline level of availability and capacity

### MIN_READY_INSTANCES = <num>
- Minimum number of instances that must be in the READY state before the service begins accepting traffic
- Default: value of MIN_INSTANCES
- Must be ≤ MIN_INSTANCES
- Useful for staged rollout or health-check gating

### MAX_INSTANCES = <num>
- Maximum number of service instances Snowflake may scale up to
- Default: value of MIN_INSTANCES (no auto-scaling beyond initial count)
- Set higher than MIN_INSTANCES to enable horizontal auto-scaling

### LOG_LEVEL = '<log_level>'
- Controls which platform event messages are ingested into the active event table
- Valid values (from most to least verbose): `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`, `OFF`
- Applies only to platform-level events, not application logs written to stdout/stderr
- Default: none specified (inherits account or database setting)

### QUERY_WAREHOUSE = <warehouse_name>
- Default warehouse used by service containers when executing Snowflake queries without specifying a warehouse explicitly
- Supports Native App object references
- Default: none

### TAG ( <tag_name> = '<tag_value>' [ , ... ] )
- Assigns one or more metadata tags to the service
- Tag values are limited to 256 characters each
- Default: none

### COMMENT = '<string_literal>'
- Free-text description of the service
- Displayed in `SHOW SERVICES` output
- Default: none

---

## Access Control Requirements
- `CREATE SERVICE` privilege on the schema
- `USAGE` privilege on the target compute pool
- `USAGE` privilege on any referenced External Access Integrations
- `READ` privilege on any referenced stages (for stage-based spec files)
- `USAGE` privilege on `QUERY_WAREHOUSE` if specified
