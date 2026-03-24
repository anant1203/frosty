# Snowflake CREATE FILE FORMAT — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY | VOLATILE } ] FILE FORMAT [ IF NOT EXISTS ] <name>
    [ TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } ]
    [ formatTypeOptions ]
    [ COMMENT = '<string_literal>' ]
```

---

## Top-Level Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| `TEMP / TEMPORARY / VOLATILE` | false | Session-scoped format when true |
| `IF NOT EXISTS` | — | Prevents error if format already exists |
| `TYPE` | CSV | File format type |
| `COMMENT` | none | Free-text description |

---

## CSV Format Type Options

### Syntax

```sql
TYPE = CSV
[ COMPRESSION = { AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE } ]
[ RECORD_DELIMITER = { '<character>' | NONE } ]
[ FIELD_DELIMITER = { '<character>' | NONE } ]
[ MULTI_LINE = { TRUE | FALSE } ]
[ FILE_EXTENSION = '<string>' ]
[ PARSE_HEADER = { TRUE | FALSE } ]
[ SKIP_HEADER = <integer> ]
[ SKIP_BLANK_LINES = { TRUE | FALSE } ]
[ DATE_FORMAT = { '<format_string>' | AUTO } ]
[ TIME_FORMAT = { '<format_string>' | AUTO } ]
[ TIMESTAMP_FORMAT = { '<format_string>' | AUTO } ]
[ BINARY_FORMAT = { HEX | BASE64 | UTF8 } ]
[ ESCAPE = { '<character>' | NONE } ]
[ ESCAPE_UNENCLOSED_FIELD = { '<character>' | NONE } ]
[ TRIM_SPACE = { TRUE | FALSE } ]
[ FIELD_OPTIONALLY_ENCLOSED_BY = { '<character>' | NONE } ]
[ NULL_IF = ( '<string>' [ , '<string>' ... ] ) ]
[ ERROR_ON_COLUMN_COUNT_MISMATCH = { TRUE | FALSE } ]
[ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
[ EMPTY_FIELD_AS_NULL = { TRUE | FALSE } ]
[ SKIP_BYTE_ORDER_MARK = { TRUE | FALSE } ]
[ ENCODING = { '<string>' | UTF8 } ]
```

### CSV Parameter Defaults

| Parameter | Default | Load | Unload | Ext Table |
|---|---|---|---|---|
| `COMPRESSION` | AUTO | yes | yes | yes |
| `RECORD_DELIMITER` | Newline (`\n`) | yes | yes | yes |
| `FIELD_DELIMITER` | `,` (comma) | yes | yes | yes |
| `MULTI_LINE` | TRUE | yes | — | yes |
| `FILE_EXTENSION` | null (uses TYPE default) | — | yes | — |
| `PARSE_HEADER` | FALSE | yes | — | — |
| `SKIP_HEADER` | 0 | yes | — | yes |
| `SKIP_BLANK_LINES` | FALSE | yes | — | yes |
| `DATE_FORMAT` | AUTO | yes | yes | — |
| `TIME_FORMAT` | AUTO | yes | yes | — |
| `TIMESTAMP_FORMAT` | AUTO | yes | yes | — |
| `BINARY_FORMAT` | HEX | yes | yes | — |
| `ESCAPE` | NONE | yes | yes | — |
| `ESCAPE_UNENCLOSED_FIELD` | `\` (backslash) | yes | yes | yes |
| `TRIM_SPACE` | FALSE | yes | — | yes |
| `FIELD_OPTIONALLY_ENCLOSED_BY` | NONE | yes | yes | yes |
| `NULL_IF` | `\N` | yes | yes | yes |
| `ERROR_ON_COLUMN_COUNT_MISMATCH` | TRUE | yes | — | — |
| `REPLACE_INVALID_CHARACTERS` | FALSE | yes | — | — |
| `EMPTY_FIELD_AS_NULL` | TRUE | yes | yes | yes |
| `SKIP_BYTE_ORDER_MARK` | TRUE | yes | — | — |
| `ENCODING` | UTF8 | yes | — | yes |

### CSV Parameter Descriptions

**COMPRESSION** — Compression algorithm for staged files. AUTO detects GZIP/BZ2/BROTLI/ZSTD/DEFLATE automatically. Use NONE for uncompressed files.

**RECORD_DELIMITER** — String or single character that separates records. Supports escape sequences (e.g., `\n`, `\r\n`). Set to NONE for single-record files.

**FIELD_DELIMITER** — Single character or string separating fields within a record. Common values: `,` (comma), `|` (pipe), `\t` (tab).

**MULTI_LINE** — When TRUE, field values may span multiple lines if enclosed. Set to FALSE to disable multi-line fields for performance.

**FILE_EXTENSION** — Override the default file extension for unloaded files (e.g., `.csv.gz`). Does not affect loading.

**PARSE_HEADER** — When TRUE, uses the first row as column names for schema detection. Requires MATCH_BY_COLUMN_NAME in COPY INTO.

**SKIP_HEADER** — Number of lines to skip at the top of each file. Use for files with header rows when PARSE_HEADER is not used.

**SKIP_BLANK_LINES** — When TRUE, blank lines are ignored. When FALSE (default), blank lines cause an error.

**DATE_FORMAT / TIME_FORMAT / TIMESTAMP_FORMAT** — Format strings for parsing/formatting date/time values. AUTO uses ISO 8601 or infers the format. Specify explicitly (e.g., `'YYYY-MM-DD'`) when files use non-standard formats.

**BINARY_FORMAT** — Encoding for binary columns: HEX (default), BASE64, or UTF8.

**ESCAPE** — Character used to escape the field enclosure character within enclosed fields. Applied only to enclosed fields; typically `\`.

**ESCAPE_UNENCLOSED_FIELD** — Escape character for fields not wrapped in the enclosure character. Default is `\` (backslash). Set to NONE to disable.

**TRIM_SPACE** — When TRUE, strips leading and trailing whitespace from string fields.

**FIELD_OPTIONALLY_ENCLOSED_BY** — Character used to optionally enclose field values. Common values: `'"'` (double-quote), `"'"` (single-quote). Set to NONE if fields are never enclosed.

**NULL_IF** — List of strings to convert to SQL NULL on load. Default is `\N`. Pass an empty list `()` to disable null substitution.

**ERROR_ON_COLUMN_COUNT_MISMATCH** — When TRUE (default), raises an error if the number of delimited columns in a row differs from the target table. Set to FALSE to allow mismatches (extra columns ignored, missing columns loaded as NULL).

**REPLACE_INVALID_CHARACTERS** — When TRUE, replaces invalid UTF-8 byte sequences with the Unicode replacement character (`\uFFFD`).

**EMPTY_FIELD_AS_NULL** — When TRUE, empty delimited fields (`,,`) are loaded as NULL. When FALSE, they are loaded as empty strings.

**SKIP_BYTE_ORDER_MARK** — When TRUE (default), ignores the UTF-8 BOM at the start of files.

**ENCODING** — Character encoding of the source files. Default is UTF8. Other supported values: ISO88591, UTF16, UTF16LE, UTF16BE, UTF32, UTF32LE, UTF32BE, BIG5, EUC_JP, EUC_KR, GB18030, GB2312, KOI8R, LATIN1, WINDOWS1250–WINDOWS1258, etc.

---

## JSON Format Type Options

### Syntax

```sql
TYPE = JSON
[ COMPRESSION = { AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE } ]
[ DATE_FORMAT = { '<format_string>' | AUTO } ]
[ TIME_FORMAT = { '<format_string>' | AUTO } ]
[ TIMESTAMP_FORMAT = { '<format_string>' | AUTO } ]
[ BINARY_FORMAT = { HEX | BASE64 | UTF8 } ]
[ TRIM_SPACE = { TRUE | FALSE } ]
[ MULTI_LINE = { TRUE | FALSE } ]
[ NULL_IF = ( '<string>' [ , '<string>' ... ] ) ]
[ ENABLE_OCTAL = { TRUE | FALSE } ]
[ ALLOW_DUPLICATE = { TRUE | FALSE } ]
[ STRIP_OUTER_ARRAY = { TRUE | FALSE } ]
[ STRIP_NULL_VALUES = { TRUE | FALSE } ]
[ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
[ IGNORE_UTF8_ERRORS = { TRUE | FALSE } ]
[ SKIP_BYTE_ORDER_MARK = { TRUE | FALSE } ]
```

### JSON Parameter Defaults

| Parameter | Default | Description |
|---|---|---|
| `COMPRESSION` | AUTO | Compression detection/algorithm |
| `DATE_FORMAT` | AUTO | For MATCH_BY_COLUMN_NAME loads |
| `TIME_FORMAT` | AUTO | For MATCH_BY_COLUMN_NAME loads |
| `TIMESTAMP_FORMAT` | AUTO | For MATCH_BY_COLUMN_NAME loads |
| `BINARY_FORMAT` | HEX | Binary column encoding |
| `TRIM_SPACE` | FALSE | Strip whitespace from strings |
| `MULTI_LINE` | TRUE | Allow newlines within JSON records |
| `NULL_IF` | `\N` | Strings treated as NULL |
| `ENABLE_OCTAL` | FALSE | Parse octal integer literals |
| `ALLOW_DUPLICATE` | FALSE | Allow duplicate object keys |
| `STRIP_OUTER_ARRAY` | FALSE | Remove outer `[...]` array wrapper |
| `STRIP_NULL_VALUES` | FALSE | Remove keys/elements with null values |
| `REPLACE_INVALID_CHARACTERS` | FALSE | Replace invalid UTF-8 bytes |
| `IGNORE_UTF8_ERRORS` | FALSE | Silently replace UTF-8 errors |
| `SKIP_BYTE_ORDER_MARK` | TRUE | Skip BOM at start of file |

**STRIP_OUTER_ARRAY** — Set to TRUE when loading a file that contains a top-level JSON array (`[{...},{...}]`); Snowflake exposes each element as a separate row.

**ALLOW_DUPLICATE** — Set to TRUE only when source files intentionally contain duplicate keys and you want last-value-wins behavior.

---

## AVRO Format Type Options

### Syntax

```sql
TYPE = AVRO
[ COMPRESSION = { AUTO | GZIP | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE } ]
[ TRIM_SPACE = { TRUE | FALSE } ]
[ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
[ NULL_IF = ( '<string>' [ , '<string>' ... ] ) ]
```

### AVRO Parameter Defaults

| Parameter | Default | Description |
|---|---|---|
| `COMPRESSION` | AUTO | Compression codec |
| `TRIM_SPACE` | FALSE | Strip whitespace (MATCH_BY_COLUMN_NAME only) |
| `REPLACE_INVALID_CHARACTERS` | FALSE | Replace invalid UTF-8 bytes |
| `NULL_IF` | `\N` | Strings treated as NULL |

> AVRO is a **load-only** format. It cannot be used for COPY INTO `<location>` (unloading).

---

## ORC Format Type Options

### Syntax

```sql
TYPE = ORC
[ TRIM_SPACE = { TRUE | FALSE } ]
[ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
[ NULL_IF = ( '<string>' [ , '<string>' ... ] ) ]
```

### ORC Parameter Defaults

| Parameter | Default | Description |
|---|---|---|
| `TRIM_SPACE` | FALSE | Strip whitespace (MATCH_BY_COLUMN_NAME only) |
| `REPLACE_INVALID_CHARACTERS` | FALSE | Replace invalid UTF-8 bytes |
| `NULL_IF` | `\N` | Strings treated as NULL |

> ORC is a **load-only** format.

---

## PARQUET Format Type Options

### Syntax

```sql
TYPE = PARQUET
[ COMPRESSION = { AUTO | LZO | SNAPPY | NONE } ]
[ BINARY_AS_TEXT = { TRUE | FALSE } ]
[ USE_LOGICAL_TYPE = { TRUE | FALSE } ]
[ USE_VECTORIZED_SCANNER = { TRUE | FALSE } ]
[ TRIM_SPACE = { TRUE | FALSE } ]
[ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
[ NULL_IF = ( '<string>' [ , '<string>' ... ] ) ]
```

### PARQUET Parameter Defaults

| Parameter | Default | Description |
|---|---|---|
| `COMPRESSION` | AUTO | Codec: AUTO, LZO, SNAPPY, NONE |
| `BINARY_AS_TEXT` | TRUE | Treat undefined binary columns as UTF-8 text |
| `USE_LOGICAL_TYPE` | — | Use Parquet logical types for load (not for unload) |
| `USE_VECTORIZED_SCANNER` | FALSE | Columnar batch scanner for improved load performance |
| `TRIM_SPACE` | FALSE | Strip whitespace (MATCH_BY_COLUMN_NAME only) |
| `REPLACE_INVALID_CHARACTERS` | FALSE | Replace invalid UTF-8 bytes |
| `NULL_IF` | `\N` | Strings treated as NULL |

**BINARY_AS_TEXT** — Set to FALSE when Parquet binary columns contain true binary data (not UTF-8 strings).

**USE_VECTORIZED_SCANNER** — Set to TRUE for large Parquet file loads to improve throughput via columnar scanning.

---

## XML Format Type Options

### Syntax

```sql
TYPE = XML
[ COMPRESSION = { AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | NONE } ]
[ IGNORE_UTF8_ERRORS = { TRUE | FALSE } ]
[ PRESERVE_SPACE = { TRUE | FALSE } ]
[ STRIP_OUTER_ELEMENT = { TRUE | FALSE } ]
[ DISABLE_AUTO_CONVERT = { TRUE | FALSE } ]
[ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
[ SKIP_BYTE_ORDER_MARK = { TRUE | FALSE } ]
```

### XML Parameter Defaults

| Parameter | Default | Description |
|---|---|---|
| `COMPRESSION` | AUTO | Compression detection/algorithm |
| `IGNORE_UTF8_ERRORS` | FALSE | Silently replace UTF-8 errors |
| `PRESERVE_SPACE` | FALSE | Keep leading/trailing whitespace in element content |
| `STRIP_OUTER_ELEMENT` | FALSE | Expose second-level elements as top-level rows |
| `DISABLE_AUTO_CONVERT` | FALSE | Disable automatic numeric/Boolean type conversion |
| `REPLACE_INVALID_CHARACTERS` | FALSE | Replace invalid UTF-8 bytes |
| `SKIP_BYTE_ORDER_MARK` | TRUE | Skip BOM at start of file |

> XML is a **load-only** format.

**STRIP_OUTER_ELEMENT** — Set to TRUE when the XML file has a wrapper root element and you want each child element loaded as a separate row.

---

## Important Constraints

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive in a single statement.
- Recreating a file format with `CREATE OR REPLACE` **breaks associations** with any external tables that reference it — use `ALTER FILE FORMAT` instead.
- Temporary/volatile formats are session-scoped and cannot be shared across sessions.
- AVRO, ORC, and XML formats support **loading only** (cannot be used for COPY INTO `<location>`).
