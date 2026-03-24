# Snowflake CREATE SCHEMA — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-schema

---

## Full Syntax

### Standard CREATE SCHEMA

```sql
CREATE [ OR REPLACE ] [ TRANSIENT ] SCHEMA [ IF NOT EXISTS ] <name>
  [ CLONE <source_schema>
      [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ] ]
  [ WITH MANAGED ACCESS ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ EXTERNAL_VOLUME = <external_volume_name> ]
  [ CATALOG = <catalog_integration_name> ]
  [ ICEBERG_VERSION_DEFAULT = <integer> ]
  [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
  [ CLASSIFICATION_PROFILE = '<classification_profile>' ]
  [ COMMENT = '<string_literal>' ]
  [ CATALOG_SYNC = '<snowflake_open_catalog_integration_name>' ]
  [ OBJECT_VISIBILITY = PRIVILEGED ]
  [ ENABLE_DATA_COMPACTION = { TRUE | FALSE } ]
  [ TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , ... ] ) ]
```

### CREATE SCHEMA … CLONE

```sql
CREATE [ OR REPLACE ] [ TRANSIENT ] SCHEMA <name>
  CLONE <source_schema>
    [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
```

Creates a zero-copy clone of an existing schema. The optional `AT | BEFORE` clause enables point-in-time cloning via Time Travel.

### CREATE OR ALTER SCHEMA (Preview Feature)

```sql
CREATE OR ALTER [ TRANSIENT ] SCHEMA <name>
  [ ... same optional parameters as CREATE SCHEMA ... ]
```

Creates the schema if it does not exist, or modifies it if it does, while preserving existing objects.

### CREATE SCHEMA … FROM BACKUP SET

```sql
CREATE SCHEMA <name> FROM BACKUP SET <backup_set> IDENTIFIER '<backup_id>'
```

Restores a schema from a Snowflake backup.

---

## Defaults Table

| Parameter | Default |
|-----------|---------|
| TRANSIENT | Permanent schema (with Fail-safe) |
| WITH MANAGED ACCESS | Disabled (standard privilege model) |
| DATA_RETENTION_TIME_IN_DAYS | 1 day (Standard: 0–1; Enterprise: 0–90) |
| MAX_DATA_EXTENSION_TIME_IN_DAYS | 14 days |
| EXTERNAL_VOLUME | None (inherits account default) |
| CATALOG | None |
| ICEBERG_VERSION_DEFAULT | 2 |
| ENABLE_ICEBERG_MERGE_ON_READ | TRUE |
| REPLACE_INVALID_CHARACTERS | FALSE |
| DEFAULT_DDL_COLLATION | None (session/account default applies) |
| STORAGE_SERIALIZATION_POLICY | OPTIMIZED |
| CLASSIFICATION_PROFILE | None |
| COMMENT | None |
| CATALOG_SYNC | None |
| OBJECT_VISIBILITY | Default (all users with USAGE can see objects) |
| ENABLE_DATA_COMPACTION | TRUE |

---

## Parameter Descriptions

### Required Parameter

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the schema within the database. Must begin with an alphabetic character. Special characters are allowed if enclosed in double quotes. |

### Type modifier

| Parameter | Description |
|-----------|-------------|
| `TRANSIENT` | Creates a schema without a Fail-safe period. All tables created inside a TRANSIENT schema are automatically transient (0–1 day Time Travel, no Fail-safe). Reduces long-term storage costs for ephemeral or staging schemas. |

### Creation modifiers

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `IF NOT EXISTS` | — | Silently succeeds if the schema already exists. Mutually exclusive with `OR REPLACE`. |
| `OR REPLACE` | — | Drops the existing schema into Time Travel before creating a new one. Mutually exclusive with `IF NOT EXISTS`. |

### CLONE variant parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `CLONE <source_schema>` | Schema name | Duplicates the source schema (zero-copy). |
| `AT ( TIMESTAMP => ... )` | Timestamp | Clone as of a specific past timestamp. |
| `AT ( OFFSET => ... )` | Seconds offset | Clone as of a relative time in the past. |
| `AT ( STATEMENT => ... )` | Query ID | Clone as of the state just after a specific statement. |
| `BEFORE ( STATEMENT => ... )` | Query ID | Clone as of the state just before a specific statement. |

### Access control

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `WITH MANAGED ACCESS` | — | Centralises privilege grants on the schema owner. Object owners within the schema can no longer grant privileges on their objects to other roles — only the schema owner can. Useful for tight governance models. |

### Time Travel and storage

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `DATA_RETENTION_TIME_IN_DAYS` | 0–1 (Standard); 0–90 (Enterprise, permanent); 0–1 (transient) | Controls the Time Travel retention window for all objects in the schema that do not override this setting. |
| `MAX_DATA_EXTENSION_TIME_IN_DAYS` | 0–90 | Maximum number of days Snowflake can automatically extend data retention to prevent stream staleness. Default: 14. |

### Iceberg / external table parameters

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `EXTERNAL_VOLUME` | Volume name | Default external volume for Iceberg tables created in this schema. |
| `CATALOG` | Catalog integration name | Default catalog integration for Iceberg tables. |
| `ICEBERG_VERSION_DEFAULT` | `2` or `3` | Default Apache Iceberg table format specification version. Default: 2. |
| `ENABLE_ICEBERG_MERGE_ON_READ` | `TRUE` / `FALSE` | When TRUE, Iceberg tables use merge-on-read for DML operations. Default: TRUE. |
| `REPLACE_INVALID_CHARACTERS` | `TRUE` / `FALSE` | When TRUE, invalid UTF-8 characters in string columns are replaced with the Unicode replacement character. Default: FALSE. |
| `STORAGE_SERIALIZATION_POLICY` | `COMPATIBLE` / `OPTIMIZED` | Controls data encoding for Iceberg tables. `OPTIMIZED` uses Snowflake-specific encodings for better performance. `COMPATIBLE` uses standard encodings for interoperability with other query engines. Default: OPTIMIZED. |
| `ENABLE_DATA_COMPACTION` | `TRUE` / `FALSE` | When TRUE, Snowflake automatically compacts small Iceberg data files. Default: TRUE. |
| `CATALOG_SYNC` | Open Catalog integration name | Syncs schema metadata to a Snowflake Open Catalog (Polaris). |

### DDL and collation defaults

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `DEFAULT_DDL_COLLATION` | Collation string | Sets the default collation for all string columns in tables created within this schema, unless overridden at the table or column level. |

### Governance and metadata

| Parameter | Valid Values | Description |
|-----------|--------------|-------------|
| `CLASSIFICATION_PROFILE` | Profile name string | Associates a data classification profile with the schema for automatic column classification. |
| `COMMENT` | String literal | Schema-level comment visible in SHOW SCHEMAS and the information schema. |
| `OBJECT_VISIBILITY` | `PRIVILEGED` | (Preview) When set, only users with explicit privileges can see the schema's objects in SHOW commands. |
| `TAG` | `tag_name = 'value'` | Attaches one or more object tags to the schema. |
| `WITH CONTACT` | `purpose = contact_name` | Associates the schema with named contacts for a given purpose. |

---

## Key Constraints

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Creating a schema automatically sets it as the active schema for the current session.
- `OR REPLACE` drops the existing schema into Time Travel before creating the new one — all objects within the old schema are also dropped.
- All tables created in a TRANSIENT schema are transient; this cannot be overridden per table.
- `WITH MANAGED ACCESS` can be added or removed at any time using `ALTER SCHEMA`.

---

## Access Control Requirements

| Privilege | Object |
|-----------|--------|
| CREATE SCHEMA | Database |
| USAGE | Database |
