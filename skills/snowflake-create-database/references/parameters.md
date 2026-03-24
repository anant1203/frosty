# Snowflake CREATE DATABASE — Parameter Reference

## Syntax Variants

```sql
-- Standard
CREATE [ OR REPLACE ] [ TRANSIENT ] DATABASE [ IF NOT EXISTS ] <name>
  [ <parameter> = <value> ... ]
  [ COMMENT = '<string>' ]

-- Clone
CREATE DATABASE <name> CLONE <source_db>
  [ AT ( TIMESTAMP => <ts> | OFFSET => <secs> | STATEMENT => <id> ) ]
  [ IGNORE TABLES WITH INSUFFICIENT DATA RETENTION ]
  [ IGNORE HYBRID TABLES ]

-- Replica
CREATE DATABASE <name> AS REPLICA OF <org_name>.<account_name>.<primary_db>
  [ DATA_RETENTION_TIME_IN_DAYS = <n> ]

-- From share
CREATE DATABASE <name> FROM SHARE <provider_account>.<share_name>

-- From listing
CREATE DATABASE <name> FROM LISTING '<listing_global_name>'
```

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| TRANSIENT | false | No Fail-safe period; reduces storage cost |
| DATA_RETENTION_TIME_IN_DAYS | 1 | 0–1 Standard; 0–90 Enterprise |
| MAX_DATA_EXTENSION_TIME_IN_DAYS | 14 | Extends retention to prevent stream staleness |
| DEFAULT_DDL_COLLATION | (none) | Inherited by all schemas/tables unless overridden |
| EXTERNAL_VOLUME | (none) | Required for Iceberg tables |
| CATALOG | (none) | Default catalog integration for Iceberg |
| ICEBERG_VERSION_DEFAULT | 2 | Set to 3 for Iceberg v3 spec |
| ENABLE_ICEBERG_MERGE_ON_READ | false | Row-level deletes for Iceberg |
| REPLACE_INVALID_CHARACTERS | false | Replace invalid UTF-8 chars in Iceberg |
| STORAGE_SERIALIZATION_POLICY | OPTIMIZED | COMPATIBLE for cross-engine interop |
| ENABLE_DATA_COMPACTION | false | Background compaction for Iceberg tables |
| CATALOG_SYNC | (none) | Sync with Snowflake Open Catalog |
| CATALOG_SYNC_NAMESPACE_MODE | NEST | NEST or FLATTEN |
| OBJECT_VISIBILITY | PRIVILEGED | Who can discover the database |
| COMMENT | (none) | Free-text description |

---

## Core Optional Parameters

### TRANSIENT
```sql
CREATE TRANSIENT DATABASE IF NOT EXISTS <name>
```
- Eliminates Fail-safe storage period (7 days normally)
- `DATA_RETENTION_TIME_IN_DAYS` is automatically set to 0
- All schemas created inside will also be transient
- Use for: temporary/scratch databases, dev environments, cost reduction

### DATA_RETENTION_TIME_IN_DAYS = <n>
- Standard edition: 0 or 1
- Enterprise edition: 0–90
- Set to 0 to disable Time Travel entirely
- Set to 0 automatically when TRANSIENT is used

### MAX_DATA_EXTENSION_TIME_IN_DAYS = <n>
- Automatically extends retention if a stream would become stale
- Prevents stream data loss during high-volume operations

### DEFAULT_DDL_COLLATION = '<spec>'
- Applies collation to all new schemas and tables by default
- Example values: `'en-ci'` (English, case-insensitive), `'utf8'`
- Does not affect existing objects

### COMMENT = '<string>'
- Free-text description displayed in Snowsight and SHOW DATABASES

---

## Iceberg Parameters
Only include these when the database will host Iceberg tables.

### EXTERNAL_VOLUME = '<volume_name>'
- Sets the default external volume for all Iceberg tables in this database
- Must have USAGE privilege on the volume

### CATALOG = '<integration_name>'
- Default catalog integration (e.g. AWS Glue, Delta)
- Must have USAGE privilege on the integration

### ICEBERG_VERSION_DEFAULT = { 2 | 3 }
- Iceberg spec version for new tables
- Default: 2; use 3 for newer Iceberg features

### ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE }
- Enables row-level delete via merge-on-read
- Default: FALSE (copy-on-write)

### REPLACE_INVALID_CHARACTERS = { TRUE | FALSE }
- Replaces invalid UTF-8 characters with the Unicode replacement character
- Default: FALSE

### STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED }
- COMPATIBLE: broader engine interoperability (Parquet v1)
- OPTIMIZED: Snowflake-optimised encoding (default)

### ENABLE_DATA_COMPACTION = { TRUE | FALSE }
- Runs background compaction on Iceberg tables
- Default: FALSE

---

## Catalog Sync Parameters
Only include when syncing with Snowflake Open Catalog.

### CATALOG_SYNC = '<open_catalog_integration_name>'
### CATALOG_SYNC_NAMESPACE_MODE = { NEST | FLATTEN }
- NEST: two-level namespace (catalog.schema)
- FLATTEN: single namespace with delimiter
### CATALOG_SYNC_NAMESPACE_FLATTEN_DELIMITER = '<char>'

---

## Visibility & Metadata

### TAG ( <tag_name> = '<tag_value>' [, ...] )
```sql
TAG (cost_center = 'engineering', env = 'prod')
```

### WITH CONTACT <contact_name>
- Associates a contact for this database

### OBJECT_VISIBILITY = { PRIVILEGED | <org_visibility> }
- Controls who can discover the database
- Requires MANAGE VISIBILITY privilege to set

---

## Replication (AS REPLICA OF)
```sql
CREATE DATABASE <secondary_name>
  AS REPLICA OF <org_name>.<account_name>.<primary_db_name>
  DATA_RETENTION_TIME_IN_DAYS = <n>;
```
- Recommended: give secondary the same name as primary
- Match DATA_RETENTION_TIME_IN_DAYS to primary

---

## Cloning (CLONE)
```sql
-- Current state
CREATE DATABASE <new_name> CLONE <source_db>;

-- Point-in-time (Time Travel)
CREATE DATABASE <new_name> CLONE <source_db>
  AT ( TIMESTAMP => '2024-01-01 00:00:00'::TIMESTAMP_LTZ );

CREATE DATABASE <new_name> CLONE <source_db>
  AT ( OFFSET => -3600 );  -- 1 hour ago

CREATE DATABASE <new_name> CLONE <source_db>
  BEFORE ( STATEMENT => '<query_id>' );
```
- `IGNORE TABLES WITH INSUFFICIENT DATA RETENTION` — skips tables whose history has expired
- `IGNORE HYBRID TABLES` — excludes hybrid tables from the clone
- Shared databases cannot be cloned

---

## Access Control Requirements
- `CREATE DATABASE` privilege (granted to SYSADMIN by default)
- `USAGE` on any EXTERNAL_VOLUME or CATALOG integration referenced
- `MANAGE VISIBILITY` to set OBJECT_VISIBILITY
