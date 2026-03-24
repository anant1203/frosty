# CREATE STREAM — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-stream

## Full Syntax

### On a Standard Table
```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [, ...] ) ]
  [ COPY GRANTS ]
  ON TABLE <table_name>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp>
                       | OFFSET => <time_difference>
                       | STATEMENT => <id>
                       | STREAM => '<name>' } ) ]
  [ APPEND_ONLY = TRUE | FALSE ]
  [ SHOW_INITIAL_ROWS = TRUE | FALSE ]
  [ COMMENT = '<string_literal>' ]
```

### On an External Table
```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [, ...] ) ]
  [ COPY GRANTS ]
  ON EXTERNAL TABLE <external_table_name>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp>
                       | OFFSET => <time_difference>
                       | STATEMENT => <id>
                       | STREAM => '<name>' } ) ]
  [ INSERT_ONLY = TRUE ]
  [ COMMENT = '<string_literal>' ]
```

### On a Directory Table (Stage)
```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [, ...] ) ]
  [ COPY GRANTS ]
  ON STAGE <stage_name>
  [ COMMENT = '<string_literal>' ]
```

### On a Dynamic Table
```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [, ...] ) ]
  [ COPY GRANTS ]
  ON DYNAMIC TABLE <table_name>
  [ COMMENT = '<string_literal>' ]
```

### On a View
```sql
CREATE [ OR REPLACE ] STREAM [ IF NOT EXISTS ] <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [, ...] ) ]
  [ COPY GRANTS ]
  ON VIEW <view_name>
  [ { AT | BEFORE } ( { TIMESTAMP => <timestamp>
                       | OFFSET => <time_difference>
                       | STATEMENT => <id>
                       | STREAM => '<name>' } ) ]
  [ APPEND_ONLY = TRUE | FALSE ]
  [ SHOW_INITIAL_ROWS = TRUE | FALSE ]
  [ COMMENT = '<string_literal>' ]
```

### Clone Variant
```sql
CREATE [ OR REPLACE ] STREAM <name>
  CLONE <source_stream>
  [ COPY GRANTS ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| `COPY GRANTS` | (not set — grants not copied) |
| `AT \| BEFORE` | (not set — stream starts at current offset) |
| `APPEND_ONLY` | `FALSE` |
| `INSERT_ONLY` | `FALSE` |
| `SHOW_INITIAL_ROWS` | `FALSE` |
| `COMMENT` | (none) |
| `TAG` | (none) |

## Parameter Descriptions

### `<name>` *(required)*
Unique identifier for the stream within its schema. Must start with an alphabetic character. Use double quotes for identifiers containing special characters (case-sensitive when quoted).

### `ON TABLE <table_name>` *(required for table streams)*
The source standard (non-external) table whose row-level changes the stream tracks.

### `ON EXTERNAL TABLE <external_table_name>` *(required for external table streams)*
The source external table. Only insert events are tracked (`INSERT_ONLY = TRUE` is required).

### `ON STAGE <stage_name>` *(required for directory table streams)*
The named stage whose directory table (file metadata) changes are monitored.

### `ON DYNAMIC TABLE <table_name>` *(required for dynamic table streams)*
The source dynamic table to track.

### `ON VIEW <view_name>` *(required for view streams)*
The source view. The stream monitors changes to the underlying base tables through the view.

### `COPY GRANTS`
When present, the replacement or cloned stream inherits all privilege grants from the original (except OWNERSHIP). Has no effect when creating a brand-new stream.

### `AT | BEFORE ( ... )`
Seeds the stream at a historical point using Time Travel. The stream's offset begins at that point, so the first query returns all changes since then.

Subparameters:
- `TIMESTAMP => <timestamp>`: Absolute point in time (`AT` is inclusive; `BEFORE` excludes that instant).
- `OFFSET => <time_difference>`: Seconds relative to now (e.g., `-3600` for one hour ago).
- `STATEMENT => <id>`: A specific query ID.
- `STREAM => '<name>'`: Matches the offset of another stream.

Constraint: Cannot reference a point before change tracking was enabled on the source object.

### `APPEND_ONLY = TRUE | FALSE`
Applicable to: standard tables and views.
- `FALSE` (default): Tracks inserts, updates, and deletes.
- `TRUE`: Tracks inserts only. Updates/deletes are ignored. Recommended for insert-heavy pipelines and for tables with geospatial columns.

### `INSERT_ONLY = TRUE`
Applicable to: external tables only. Required; external tables only produce insert-type change records (cloud storage deletions are not surfaced as DELETE rows).

### `SHOW_INITIAL_ROWS = TRUE | FALSE`
- `FALSE` (default): Stream starts empty; only future changes appear.
- `TRUE`: The first consumption of the stream returns all rows currently in the source table as INSERT records. Subsequent queries show normal changes.

### `COMMENT = '<string_literal>'`
Free-text description of the stream. Visible in `SHOW STREAMS` output and the Snowsight UI.

### `TAG ( <tag_name> = '<tag_value>' [, ...] )`
Attaches governance tags to the stream. Tag values are strings up to 256 characters.

## Metadata Columns
Every stream automatically adds three metadata columns to query results:

| Column | Type | Description |
|--------|------|-------------|
| `METADATA$ACTION` | STRING | `INSERT` or `DELETE` |
| `METADATA$ISUPDATE` | BOOLEAN | `TRUE` when the row is part of an UPDATE operation |
| `METADATA$ROW_ID` | STRING | Stable unique identifier for the source row |

## Key Behavioral Notes

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive; never use both.
- Stream offsets advance when a DML statement that consumes the stream commits. Use explicit transactions to ensure consistent reads across multiple queries in the same batch.
- Only one task should consume a given stream. For multiple consumers, create separate streams on the same source table.
- Geospatial column changes cannot be retrieved via standard streams; use `APPEND_ONLY = TRUE` instead.
