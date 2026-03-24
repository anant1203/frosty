# CREATE CORTEX SEARCH SERVICE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-cortex-search

---

## Full Syntax

### Single-Index Syntax (keyword/semantic search on one text column)

```sql
CREATE [ OR REPLACE ] CORTEX SEARCH SERVICE [ IF NOT EXISTS ] <name>
  ON <search_column>
  [ PRIMARY KEY ( <col_name> [, ...] ) ]
  ATTRIBUTES <col_name> [, ...]
  WAREHOUSE = <warehouse_name>
  TARGET_LAG = '<num> { seconds | minutes | hours | days }'
  [ EMBEDDING_MODEL = <embedding_model_name> ]
  [ REFRESH_MODE = { FULL | INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ FULL_INDEX_BUILD_INTERVAL_DAYS = <num> ]
  [ COMMENT = '<comment>' ]
AS <query>;
```

### Multi-Index Syntax (hybrid keyword + vector search)

```sql
CREATE [ OR REPLACE ] CORTEX SEARCH SERVICE <name>
  TEXT INDEXES <text_column_name> [, ...]
  VECTOR INDEXES <column_specification> [, ...]
  [ PRIMARY KEY ( <col_name> [, ...] ) ]
  ATTRIBUTES <col_name> [, ...]
  WAREHOUSE = <warehouse_name>
  TARGET_LAG = '<num> { seconds | minutes | hours | days }'
  [ REFRESH_MODE = { FULL | INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ FULL_INDEX_BUILD_INTERVAL_DAYS = <num> ]
  [ COMMENT = '<comment>' ]
AS <query>;
```

---

## Defaults Table

| Parameter | Default Value |
|---|---|
| `OR REPLACE` | Not set |
| `IF NOT EXISTS` | Not set |
| `PRIMARY KEY` | None |
| `EMBEDDING_MODEL` | `snowflake-arctic-embed-m-v1.5` |
| `REFRESH_MODE` | `INCREMENTAL` |
| `INITIALIZE` | `ON_CREATE` |
| `FULL_INDEX_BUILD_INTERVAL_DAYS` | `0` (no scheduled full rebuild) |
| `COMMENT` | None |

---

## Parameter Descriptions

### `name`
Unique identifier for the Cortex Search Service within the schema. Must start with an alphabetic character. Case-insensitive by default unless double-quoted.

### `ON search_column` (single-index only)
**Required for single-index syntax.** The text column from the query result set on which Snowflake builds the search index. Must be a plain text (VARCHAR) column. Only one column may be specified in this position; use the multi-index syntax for multiple text columns.

### `TEXT INDEXES` (multi-index only)
**Required for multi-index syntax.** Comma-separated list of text column names on which keyword BM25-style indexes are built. Columns must appear in the `AS <query>` result set.

### `VECTOR INDEXES` (multi-index only)
**Required for multi-index syntax.** Comma-separated list of columns or column specifications for dense vector similarity indexes. Supports:
- Managed embeddings: specify a VARCHAR column and Snowflake generates embeddings automatically.
- User-provided embeddings: specify a VECTOR(FLOAT, N) column.
At least one `VECTOR INDEXES` column is required when using the multi-index form.

### `PRIMARY KEY`
Optional. One or more text columns that uniquely identify each row in the underlying query. Providing a primary key enables optimized incremental refresh — only rows whose primary key has changed since the last refresh are reprocessed. Strongly recommended when the source table has a natural unique key.

### `ATTRIBUTES`
**Required.** Comma-separated list of columns that can be used as filters when querying the service via the REST API or SQL. These columns are stored alongside the index data. Any column from the `AS <query>` result set is valid.

### `WAREHOUSE`
**Required.** Name of the virtual warehouse used to execute the `AS <query>` and to perform index refresh operations. Larger warehouses reduce initial build time and refresh latency.

### `TARGET_LAG`
**Required.** Maximum acceptable lag between source table updates and the Cortex Search index. Format: `'<num> { seconds | minutes | hours | days }'`. Examples: `'1 hour'`, `'30 minutes'`, `'2 days'`. Snowflake schedules refreshes to keep the index within this lag window.

### `EMBEDDING_MODEL` (single-index only)
Name of the embedding model used to generate vector representations of the search column text. Valid values include:
- `snowflake-arctic-embed-m-v1.5` (default, ~110M parameters, English-optimized)
- `snowflake-arctic-embed-l-v2.0` (large model, higher recall)
- Other Snowflake-supported Cortex embedding models as announced in release notes.
Not applicable to the multi-index syntax (each VECTOR INDEXES column specifies its own model or uses pre-built vectors).

### `REFRESH_MODE`
Controls the strategy used when refreshing the index after source data changes.
- `INCREMENTAL` (default): only processes changed rows, using change-tracking on the source table. Automatically enables change tracking on the source table.
- `FULL`: rebuilds the entire index from scratch on every refresh. Use when the source query is a complex transformation that does not support incremental computation.

### `INITIALIZE`
Determines when the initial index build occurs after the service is created.
- `ON_CREATE` (default): Snowflake begins the first full index build immediately after the `CREATE` statement completes.
- `ON_SCHEDULE`: the first build is deferred until the scheduled refresh window. Use when you want to control resource consumption at creation time.

### `FULL_INDEX_BUILD_INTERVAL_DAYS`
Soft target for how many days elapse between periodic full index rebuilds, even when `REFRESH_MODE = INCREMENTAL`. Default `0` disables scheduled full rebuilds. Set to a positive integer (e.g., `7`) to periodically compact and optimize the index.

### `COMMENT`
Optional free-text description of the service. Visible in `SHOW CORTEX SEARCH SERVICES` and `DESCRIBE CORTEX SEARCH SERVICE`.

### `AS <query>`
**Required.** A `SELECT` statement whose result set provides the data for the index. The query may join multiple tables, apply filters, or compute derived columns. The columns referenced in `ON`, `TEXT INDEXES`, `VECTOR INDEXES`, `PRIMARY KEY`, and `ATTRIBUTES` must all appear in this query's output. Change tracking is automatically enabled on base tables when `REFRESH_MODE = INCREMENTAL`.

---

## Usage Notes

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- The service owner role must have `CREATE CORTEX SEARCH SERVICE` privilege on the schema and `USAGE` on the warehouse.
- Querying the service requires `USAGE` on the service object; use the `SNOWFLAKE.CORTEX.SEARCH_PREVIEW` function or the Cortex Search REST API.
- Multi-index services support hybrid retrieval: combine BM25 keyword scores (TEXT INDEXES) with cosine similarity scores (VECTOR INDEXES) and re-rank with RRF or a custom re-ranker.
