# CREATE EXTERNAL TABLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-external-table

---

## Full Syntax

### Variant 1 — Partitions computed from expressions (supports auto-refresh)

```sql
CREATE [ OR REPLACE ] EXTERNAL TABLE [ IF NOT EXISTS ] <table_name>
  ( <col_name> <col_type> AS <expr> [ , <col_name> <col_type> AS <expr> , ... ] )
  [ PARTITION BY ( <partition_col> [, <partition_col> , ...] ) ]
  [ WITH ] LOCATION = @[<namespace>.]<ext_stage_name>[/<path>]
  [ REFRESH_ON_CREATE = { TRUE | FALSE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ PATTERN = '<regex_pattern>' ]
  FILE_FORMAT = (
    { FORMAT_NAME = '<file_format_name>'
    | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] }
  )
  [ AWS_SNS_TOPIC = '<sns_topic_arn>' ]
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( VALUE ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

### Variant 2 — Partitions added manually (USER_SPECIFIED)

```sql
CREATE [ OR REPLACE ] EXTERNAL TABLE [ IF NOT EXISTS ] <table_name>
  ( <col_name> <col_type> AS <expr> [ , ... ] )
  PARTITION BY ( <partition_col> [, ...] )
  PARTITION_TYPE = USER_SPECIFIED
  [ WITH ] LOCATION = @[<namespace>.]<ext_stage_name>[/<path>]
  [ REFRESH_ON_CREATE = { TRUE | FALSE } ]
  FILE_FORMAT = (
    { FORMAT_NAME = '<file_format_name>'
    | TYPE = { CSV | JSON | AVRO | ORC | PARQUET } [ formatTypeOptions ] }
  )
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( VALUE ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

### Variant 3 — Delta Lake

```sql
CREATE [ OR REPLACE ] EXTERNAL TABLE [ IF NOT EXISTS ] <table_name>
  ( <col_name> <col_type> AS <expr> [ , ... ] )
  [ PARTITION BY ( <partition_col> [, ...] ) ]
  [ WITH ] LOCATION = @[<namespace>.]<ext_stage_name>[/<path>]
  [ REFRESH_ON_CREATE = { TRUE | FALSE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  TABLE_FORMAT = DELTA
  FILE_FORMAT = ( TYPE = PARQUET [ formatTypeOptions ] )
  [ COPY GRANTS ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( VALUE ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

---

## Defaults Table

| Parameter | Default | Notes |
|-----------|---------|-------|
| `LOCATION` | **Required** — no default | Must reference an external stage (S3, Azure, GCS) |
| `FILE_FORMAT` | **Required** — no default | `TYPE = CSV` if not specifying FORMAT_NAME |
| `REFRESH_ON_CREATE` | `TRUE` | Auto-refreshes metadata immediately after CREATE |
| `AUTO_REFRESH` | `TRUE` | Enables event-triggered metadata refreshes |
| `PATTERN` | None | Regex filter applied to staged file paths |
| `PARTITION_TYPE` | Expression-based (not USER_SPECIFIED) | Set to `USER_SPECIFIED` for manual partition management |
| `TABLE_FORMAT` | Standard (non-Delta) | Set to `DELTA` for Delta Lake tables |
| `AWS_SNS_TOPIC` | None | Required for S3 auto-refresh via SNS notifications |
| `COPY GRANTS` | Not set | Retain privileges from replaced table |
| `COMMENT` | None | Free-text table description |
| `ROW ACCESS POLICY` | None | Row-level security; reference `VALUE` column |
| `TAG` | None | Metadata tags as name=value pairs |

---

## Parameter Descriptions

### LOCATION *(required)*
Specifies the external stage and optional sub-path containing the data files.

- Format: `@[<namespace>.]<ext_stage_name>[/<path>]`
- Must be an **external** stage (Amazon S3, Azure Blob Storage / ADLS, or Google Cloud Storage).
- Internal Snowflake stages are **not** supported.

### FILE_FORMAT *(required)*
Defines how staged files are parsed. Two forms:

1. **Named format**: `FORMAT_NAME = '<existing_file_format_name>'`
2. **Inline format**: `TYPE = { CSV | JSON | AVRO | ORC | PARQUET }` followed by optional format-specific options.

Common inline options:

| Option | Applies to | Default | Description |
|--------|-----------|---------|-------------|
| `COMPRESSION` | All | `AUTO` | `AUTO`, `GZIP`, `BZ2`, `BROTLI`, `ZSTD`, `DEFLATE`, `RAW_DEFLATE`, `NONE` |
| `REPLACE_INVALID_CHARACTERS` | All | `FALSE` | Replace invalid UTF-8 bytes with replacement character |
| `FIELD_DELIMITER` | CSV | `,` | Column delimiter |
| `RECORD_DELIMITER` | CSV | `\n` | Row delimiter |
| `SKIP_HEADER` | CSV | `0` | Number of header rows to skip |
| `NULL_IF` | CSV | `\\N` | Strings to treat as SQL NULL |
| `TRIM_SPACE` | CSV | `FALSE` | Strip leading/trailing whitespace |

### Column Definitions (virtual columns)
All columns in an external table are **virtual** — computed from expressions, not stored physically.

Key pseudocolumns available inside expressions:

| Pseudocolumn | Type | Description |
|-------------|------|-------------|
| `VALUE` | VARIANT | One row from the staged file (entire row as JSON/CSV variant) |
| `METADATA$FILENAME` | STRING | Path of the staged file relative to the stage root |
| `METADATA$FILE_ROW_NUMBER` | INTEGER | Row number within the file (1-based) |

Example column definitions:

```sql
-- CSV: reference positional columns c1, c2, ...
id    NUMBER   AS (value:c1::NUMBER),
name  VARCHAR  AS (value:c2::VARCHAR),

-- Semi-structured: dot-path notation
city  VARCHAR  AS (value:"address"."city"::VARCHAR),

-- Partition column from filename
dt    DATE     AS (TO_DATE(SPLIT_PART(METADATA$FILENAME, '/', 3), 'YYYY-MM-DD'))
```

### PARTITION BY
One or more virtual column expressions used to partition the metadata. Improves performance of queries with selective predicates on partition columns.

### PARTITION_TYPE
- Omit (default): partitions are computed automatically from PARTITION BY expressions.
- `USER_SPECIFIED`: partitions must be added manually via `ALTER EXTERNAL TABLE … ADD PARTITION`.

### REFRESH_ON_CREATE
When `TRUE` (default), Snowflake immediately scans the stage and populates table metadata after the CREATE statement. Set to `FALSE` to defer the initial scan.

### AUTO_REFRESH
When `TRUE` (default), Snowflake automatically refreshes metadata in response to cloud storage event notifications (e.g., S3 event notifications, Azure Event Grid, GCS Pub/Sub). Requires cloud-side notification configuration.

### PATTERN
A regular expression applied to staged file paths (relative to the stage root). Only files whose paths match the regex are included.

Example: `PATTERN = '.*[.]csv'`

### AWS_SNS_TOPIC
The ARN of the Amazon SNS topic used to deliver S3 event notifications for auto-refresh on AWS. Required when `AUTO_REFRESH = TRUE` and the stage is on S3.

### TABLE_FORMAT = DELTA
Declares that the external table reads Delta Lake format files. Requires `FILE_FORMAT = (TYPE = PARQUET)`.

### COPY GRANTS
When using `CREATE OR REPLACE`, retains access privileges from the original external table.

### ROW ACCESS POLICY
Applies a row-level security policy. For external tables, reference the `VALUE` column in the policy expression, not individual virtual columns.

---

## Important Usage Notes

- External tables support **external stages only** (S3, Azure, GCS); internal stages are unsupported.
- Snowflake does **not** enforce integrity constraints (including NOT NULL) on external tables.
- **Unsupported features**: Time Travel, clustering keys, cloning, XML file format.
- `OR REPLACE` is equivalent to `DROP EXTERNAL TABLE` + `CREATE` — it does **not** preserve the old table in Fail-Safe.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- DML operations (INSERT, UPDATE, DELETE) are not supported on external tables.
