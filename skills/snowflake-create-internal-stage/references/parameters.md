# Snowflake CREATE STAGE (Internal) — Parameter Reference

## Syntax

```sql
-- Named internal stage (can be created with DDL)
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] STAGE [ IF NOT EXISTS ] <internal_stage_name>
    [ ENCRYPTION = ( TYPE = 'SNOWFLAKE_FULL' | TYPE = 'SNOWFLAKE_SSE' ) ]
    [ DIRECTORY = (
        ENABLE = { TRUE | FALSE }
        [ AUTO_REFRESH = { TRUE | FALSE } ]
      ) ]
    [ FILE_FORMAT = (
        { FORMAT_NAME = '<file_format_name>'
          | TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML | CUSTOM }
            [ formatTypeOptions ]
        }
      ) ]
    [ COMMENT = '<string_literal>' ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
```

> **Note:** User stages (`@~`) and table stages (`@%<table_name>`) are created automatically by Snowflake and cannot be created, replaced, or dropped via DDL. They can be used with PUT, GET, LIST, REMOVE, and COPY INTO commands directly.

---

## Stage Types Comparison

| Stage Type | Created By | Scope | Use Case |
|---|---|---|---|
| User stage (`@~`) | Snowflake (automatic) | Per user | Files for a single user's personal use |
| Table stage (`@%<table>`) | Snowflake (automatic) | Per table | Files staged for a specific table |
| Named internal stage | DDL (`CREATE STAGE`) | Schema-level | Shared data loading across tables/users |

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| `TEMP / TEMPORARY` | false | Stage dropped at end of session when true |
| `IF NOT EXISTS` | — | Prevents error if stage already exists |
| `ENCRYPTION TYPE` | `SNOWFLAKE_FULL` | Both client-side and server-side encryption |
| `DIRECTORY ENABLE` | FALSE | Enables directory table for file browsing |
| `DIRECTORY AUTO_REFRESH` | FALSE | Not applicable to internal stages (no cloud events) |
| `FILE_FORMAT TYPE` | CSV | Default format when not specified on COPY INTO |
| `COMMENT` | none | Free-text description |

---

## Detailed Parameter Descriptions

### ENCRYPTION

Specifies the encryption method for files stored in the internal stage.

```sql
ENCRYPTION = ( TYPE = 'SNOWFLAKE_FULL' )   -- default
ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' )
```

- **SNOWFLAKE_FULL** (default): Both client-side encryption (before upload) and server-side encryption (at rest). Provides the highest level of data protection.
- **SNOWFLAKE_SSE**: Server-side encryption only. Files are encrypted at rest by Snowflake but are not encrypted before being sent over the network.
- Choose `SNOWFLAKE_SSE` only when client-side encryption is incompatible with your toolchain or when performance is a priority over maximum security.

### DIRECTORY

Creates a directory table that catalogs files in the stage.

```sql
DIRECTORY = ( ENABLE = TRUE )
```

- `ENABLE = TRUE`: Activates the directory table, allowing `SELECT * FROM DIRECTORY(@stage)` and `LIST @stage` queries.
- `AUTO_REFRESH`: Not meaningful for internal stages (no cloud event notifications); leave at default FALSE.
- Enable only when you need to query metadata about staged files (file name, size, last modified, etag).

### FILE_FORMAT

Defines the default file format for COPY INTO operations that reference this stage without an explicit format clause.

```sql
-- Reference a named format
FILE_FORMAT = ( FORMAT_NAME = 'my_json_format' )

-- Inline format specification
FILE_FORMAT = ( TYPE = JSON NULL_IF = () STRIP_OUTER_ARRAY = TRUE )
```

- If omitted, COPY INTO operations must specify their own format or rely on the default CSV behavior.
- Named formats are preferred for reuse across multiple stages and tables.
- See the `snowflake-create-file-format` skill for the full list of format type options.

#### Common CSV formatTypeOptions for Internal Stages

| Parameter | Default | Description |
|---|---|---|
| `COMPRESSION` | AUTO | Compression codec: AUTO, GZIP, BZ2, BROTLI, ZSTD, DEFLATE, RAW_DEFLATE, NONE |
| `RECORD_DELIMITER` | Newline | Character separating records |
| `FIELD_DELIMITER` | `,` (comma) | Character separating fields |
| `SKIP_HEADER` | 0 | Number of header lines to skip |
| `SKIP_BLANK_LINES` | FALSE | Skip blank lines in input |
| `FIELD_OPTIONALLY_ENCLOSED_BY` | NONE | Quote character wrapping field values |
| `NULL_IF` | `\N` | String values treated as NULL |
| `EMPTY_FIELD_AS_NULL` | TRUE | Empty strings loaded as NULL |
| `TRIM_SPACE` | FALSE | Strip leading/trailing whitespace |
| `ERROR_ON_COLUMN_COUNT_MISMATCH` | TRUE | Raise error when column count differs |
| `DATE_FORMAT` | AUTO | Date parsing format string |
| `TIME_FORMAT` | AUTO | Time parsing format string |
| `TIMESTAMP_FORMAT` | AUTO | Timestamp parsing format string |
| `ENCODING` | UTF8 | Character encoding |

### TEMP / TEMPORARY

```sql
CREATE TEMPORARY STAGE my_temp_stage;
```

- Stage is automatically dropped at the end of the current Snowflake session.
- Useful for one-off or scripted data loads where cleanup is desired.
- Cannot be shared across sessions.

### COMMENT = `'<string>'`

- Free-text description displayed in `SHOW STAGES` and Snowsight.
- Best practice: include the owning team, purpose, and related tables.

### TAG

```sql
[ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] )
```

- Key-value metadata for governance, cost attribution, and data classification.
- Example: `TAG (environment = 'prod', pii = 'false')`.

---

## Access Control Requirements

- `CREATE STAGE` privilege on the target schema.
- `READ` privilege on the stage to use `LIST`, `GET`, `COPY INTO <table>`.
- `WRITE` privilege on the stage to use `PUT`, `REMOVE`, `COPY INTO <location>`.
- `USAGE` on the database and schema containing the stage.

---

## Usage Notes

- Files on internal named stages persist until explicitly removed with `REMOVE @stage`.
- Use `PUT file://local/path @stage` to upload files from a client.
- Use `GET @stage file://local/path` to download files to a client.
- Files on user/table stages follow the same PUT/GET/LIST/REMOVE/COPY INTO commands but require no DDL to set up.
