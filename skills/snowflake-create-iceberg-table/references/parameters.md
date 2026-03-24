# CREATE ICEBERG TABLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table

---

## Full Syntax

### Variant 1 — Snowflake as Iceberg catalog (most common)

```sql
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  (
    <col_name> <col_type> [ DEFAULT <col_default> ]
      [ inlineConstraint ]
      [ NOT NULL ]
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , ... ) ] ]
      [ [ WITH ] PROJECTION POLICY <policy_name> ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
      [ COMMENT '<string_literal>' ]
    [ , <col_name> <col_type> [ ... ] ]
    [ , outoflineConstraint [ ... ] ]
  )
  [ PARTITION BY ( <partitionExpression> [, ...] ) ]
  [ PATH_LAYOUT = { FLAT | HIERARCHICAL } ]
  [ CLUSTER BY ( <expr> [ , ... ] ) ]
  [ EXTERNAL_VOLUME = '<external_volume_name>' ]
  [ CATALOG = 'SNOWFLAKE' ]
  [ BASE_LOCATION = '<directory_for_table_files>' ]
  [ TARGET_FILE_SIZE = '{ AUTO | 16MB | 32MB | 64MB | 128MB }' ]
  [ CATALOG_SYNC = '<open_catalog_integration_name>' ]
  [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ ICEBERG_VERSION = <integer> ]
  [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , ... ] ) ]
  [ ENABLE_DATA_COMPACTION = { TRUE | FALSE } ]
```

### Variant 2 — CREATE AS SELECT (CTAS)

```sql
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  [ ... column definitions and table options ... ]
  AS SELECT <query>
```

### Variant 3 — CREATE LIKE (clone structure only)

```sql
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  LIKE <source_table>
  [ ... table options ... ]
```

### Variant 4 — External catalog (REST / Snowflake Open Catalog / Delta / object storage)

```sql
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  EXTERNAL_VOLUME = '<external_volume_name>'
  CATALOG = '<catalog_integration_name>'
  [ CATALOG_TABLE_NAME = '<catalog_table_name>' ]
  [ CATALOG_NAMESPACE = '<catalog_namespace>' ]
  [ METADATA_FILE_PATH = '<metadata_file_path>' ]
  [ BASE_LOCATION = '<path>' ]
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ COPY GRANTS ]
```

---

## Defaults Table

| Parameter | Default | Notes |
|-----------|---------|-------|
| `EXTERNAL_VOLUME` | Account/schema default (if set) | Specifies where table files are stored |
| `CATALOG` | `'SNOWFLAKE'` | Use a catalog integration name for external catalogs |
| `BASE_LOCATION` | None (required for Snowflake catalog) | Sub-path within the external volume |
| `PARTITION BY` | None | Omit for unpartitioned tables |
| `PATH_LAYOUT` | `HIERARCHICAL` | `FLAT` stores all files in one directory |
| `CLUSTER BY` | None | Do not add unless the table will be very large |
| `TARGET_FILE_SIZE` | `AUTO` | `AUTO`, `16MB`, `32MB`, `64MB`, `128MB` |
| `CATALOG_SYNC` | None | Open Catalog integration name for catalog sync |
| `STORAGE_SERIALIZATION_POLICY` | `COMPATIBLE` | Use `OPTIMIZED` only when Snowflake-only read/write is acceptable |
| `DATA_RETENTION_TIME_IN_DAYS` | `1` | Range: 0–90 (Enterprise); 0–1 (Standard) |
| `MAX_DATA_EXTENSION_TIME_IN_DAYS` | Inherited from account/schema | Extends retention to prevent stream staleness |
| `CHANGE_TRACKING` | `FALSE` | Enable for streams and change data capture |
| `ICEBERG_VERSION` | Latest supported version | Iceberg spec version (e.g., `2`) |
| `ENABLE_ICEBERG_MERGE_ON_READ` | `FALSE` | Enables merge-on-read for DML operations |
| `ENABLE_DATA_COMPACTION` | `TRUE` | Enables automatic background compaction |
| `COPY GRANTS` | Not set | Retain privileges from replaced table |
| `COMMENT` | None | Free-text table description |
| `ROW ACCESS POLICY` | None | Row-level security |
| `AGGREGATION POLICY` | None | Aggregation-level security |
| `TAG` | None | Metadata tags |

---

## Parameter Descriptions

### table_name *(required)*
Unique identifier for the Iceberg table within the schema. Must start with an alphabetic character.

### col_name / col_type *(required for explicit column definition)*
Column name and SQL data type. Refer to Snowflake's data type reference. Iceberg has its own type mapping; Snowflake translates SQL types to Iceberg types in the table metadata.

### DEFAULT \<col_default\>
Default value assigned to the column on INSERT when no value is supplied. Supports literals and simple expressions.

### NOT NULL
Prevents the column from accepting NULL values. Note: NOT NULL and UNIQUE constraints on PRIMARY KEY columns are represented as **identifier fields** in Iceberg metadata, but Snowflake does **not enforce** them at DML time for Iceberg tables.

### inlineConstraint / outoflineConstraint
Constraint syntax (PRIMARY KEY, UNIQUE, FOREIGN KEY) follows standard Snowflake DDL. These constraints are stored as Iceberg metadata identifier fields but are **not enforced** by Snowflake DML.

### MASKING POLICY
Applies a column-level data masking policy.

### PROJECTION POLICY
Controls whether the column can be projected (returned) in queries.

### PARTITION BY
Defines partitioning using Iceberg partition transforms:

| Transform | Syntax | Description |
|-----------|--------|-------------|
| Identity | `IDENTIFIER(<col>)` | Partition per distinct value |
| Bucket | `BUCKET(<n>, <col>)` | Hash into n buckets |
| Truncate | `TRUNCATE(<n>, <col>)` | Truncate string/int to width n |
| Year | `YEAR(<col>)` | Year extracted from timestamp/date |
| Month | `MONTH(<col>)` | Month extracted from timestamp/date |
| Day | `DAY(<col>)` | Day extracted from timestamp/date |
| Hour | `HOUR(<col>)` | Hour extracted from timestamp |

### PATH_LAYOUT
Controls how data files are written within the external volume.

- `HIERARCHICAL` (default): files are written into a directory hierarchy matching the partition structure.
- `FLAT`: all files are written into a single directory regardless of partitioning.

### CLUSTER BY
Defines a Snowflake-level clustering key for the Iceberg table, improving query pruning on large tables. Not recommended unless the table is expected to be very large (multi-terabyte).

### EXTERNAL_VOLUME
Name of the external volume (pre-configured cloud storage integration) where Iceberg table files and metadata will be written. Must be set at account or schema level if not specified inline.

### CATALOG
Specifies the Iceberg catalog:

- `'SNOWFLAKE'` (default): Snowflake manages all Iceberg metadata.
- `'<catalog_integration_name>'`: delegates catalog management to an external system (e.g., AWS Glue, Apache Polaris, REST catalog).

### BASE_LOCATION
Sub-path within the external volume's storage location where the table's files will be stored. Required when `CATALOG = 'SNOWFLAKE'`.

### TARGET_FILE_SIZE
Target size for individual Parquet data files.

| Value | Description |
|-------|-------------|
| `AUTO` (default) | Snowflake determines optimal size |
| `16MB` | Use for workloads with many small writes |
| `32MB` | Moderate file size |
| `64MB` | Moderate-large file size |
| `128MB` | Large files; reduces metadata overhead for bulk workloads |

### CATALOG_SYNC
Name of an Open Catalog integration for syncing the Snowflake-managed Iceberg table to an external catalog (e.g., Apache Polaris).

### STORAGE_SERIALIZATION_POLICY
Controls encoding and compression of data files.

| Value | Description |
|-------|-------------|
| `COMPATIBLE` (default) | Uses broadly compatible encodings; readable by non-Snowflake engines |
| `OPTIMIZED` | Uses Snowflake-optimized encodings; may not be readable by all external engines |

### DATA_RETENTION_TIME_IN_DAYS
Number of days historical data is retained for Time Travel. Range: `0–90` (Enterprise); `0–1` (Standard).

### MAX_DATA_EXTENSION_TIME_IN_DAYS
Maximum number of extra days Snowflake may extend retention to prevent streams from becoming stale.

### CHANGE_TRACKING
When `TRUE`, enables Snowflake streams on the Iceberg table for change data capture. Default: `FALSE`.

### ICEBERG_VERSION
Specifies the Iceberg specification version (e.g., `1` or `2`). Defaults to the latest version supported by Snowflake.

### ENABLE_ICEBERG_MERGE_ON_READ
When `TRUE`, uses merge-on-read semantics for DML operations. Default: `FALSE` (copy-on-write).

### ENABLE_DATA_COMPACTION
When `TRUE` (default), Snowflake runs background compaction to merge small files. Disable only if you manage compaction externally.

### COPY GRANTS
When using `CREATE OR REPLACE`, retains access privileges from the original Iceberg table.

### ROW ACCESS POLICY
Applies a row-level security policy. Syntax: `WITH ROW ACCESS POLICY <policy_name> ON (<col_name> [, ...])`.

### AGGREGATION POLICY
Applies an aggregation-level security policy.

### TAG
Assigns object metadata tags. Format: `TAG (<tag_name> = '<tag_value>' [, ...])`. Values must be 256 characters or fewer.

---

## Important Usage Notes

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- `NOT NULL` and `UNIQUE` constraints on PRIMARY KEY columns are stored in Iceberg metadata as identifier fields but are **not enforced** by Snowflake DML.
- When `CATALOG = 'SNOWFLAKE'`, both `EXTERNAL_VOLUME` and `BASE_LOCATION` are effectively required (unless set at the schema/account level).
- `STORAGE_SERIALIZATION_POLICY = OPTIMIZED` improves query performance but produces files that may not be readable by non-Snowflake query engines.
- For CTAS, the column types are inferred from the SELECT query.
