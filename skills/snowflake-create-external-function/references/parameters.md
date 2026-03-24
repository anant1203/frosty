# CREATE EXTERNAL FUNCTION — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-external-function

---

## Full Syntax

```sql
CREATE [ OR REPLACE ] [ SECURE ] EXTERNAL FUNCTION <name>
  ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS <result_data_type>
  [ [ NOT ] NULL ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ COMMENT = '<string_literal>' ]
  API_INTEGRATION = <api_integration_name>
  [ HEADERS = ( '<header_1>' = '<value_1>' [ , '<header_2>' = '<value_2>' ... ] ) ]
  [ CONTEXT_HEADERS = ( <context_function_1> [ , <context_function_2> ... ] ) ]
  [ MAX_BATCH_ROWS = <integer> ]
  [ COMPRESSION = <compression_type> ]
  [ REQUEST_TRANSLATOR = <request_translator_udf_name> ]
  [ RESPONSE_TRANSLATOR = <response_translator_udf_name> ]
  AS '<url_of_proxy_and_resource>';
```

---

## Defaults Table

| Parameter | Default Value |
|---|---|
| `OR REPLACE` | Not set (error if function with same signature exists) |
| `SECURE` | Not set (URL and headers visible to authorized roles) |
| `NULL / NOT NULL` | `NULL` (function may return NULL) |
| `CALLED ON NULL INPUT` | `CALLED ON NULL INPUT` (function always invoked) |
| `VOLATILE / IMMUTABLE` | `VOLATILE` |
| `COMMENT` | `'user-defined function'` |
| `HEADERS` | None |
| `CONTEXT_HEADERS` | None |
| `MAX_BATCH_ROWS` | Auto-estimated by Snowflake |
| `COMPRESSION` | `AUTO` (Snowflake selects GZIP or NONE based on payload) |
| `REQUEST_TRANSLATOR` | None (Snowflake row-array envelope used as-is) |
| `RESPONSE_TRANSLATOR` | None (Snowflake expects standard row-array response) |

---

## Parameter Descriptions

### `name`
Identifier for the external function. The signature (name + argument data types) must be unique within the schema. Use double-quoted identifiers for case-sensitive or special-character names.

### `arg_name arg_data_type`
Input argument name and its Snowflake SQL data type. Parentheses are always required even when there are no arguments: `()`. GEOGRAPHY is not supported as an argument or return type.

### `RETURNS result_data_type`
**Required.** The SQL data type returned by the external function. GEOGRAPHY is not supported.

### `NOT NULL`
Asserts that the function never returns NULL. Informational only — not enforced at runtime.

### `OR REPLACE`
Atomically replaces an existing external function with the same signature. Prefer `IF NOT EXISTS` for idempotent scripts. Note: `IF NOT EXISTS` is **not supported** for external functions — use `OR REPLACE` or omit both clauses.

### `SECURE`
Hides the proxy URL, HTTP headers, and context headers from roles that do not own the function. Use when the endpoint URL or headers contain sensitive information (API keys embedded in headers, proprietary endpoint paths).

### `CALLED ON NULL INPUT` (default)
The external function is always called, even when one or more arguments are NULL. The remote service must handle NULL values.

### `RETURNS NULL ON NULL INPUT` / `STRICT`
The function is not invoked when any argument is NULL; Snowflake returns NULL automatically without making an HTTP call. Equivalent aliases. Use to avoid unnecessary remote calls and to protect endpoints that cannot accept NULLs.

### `VOLATILE` (default)
Snowflake assumes the function may return different results for the same inputs and does not cache results between rows.

### `IMMUTABLE`
Declares that the function always returns the same output for the same inputs. Snowflake may optimize by caching results. This is a hint — not enforced.

### `COMMENT`
Optional free-text description visible in `SHOW EXTERNAL FUNCTIONS` output. Default: `'user-defined function'`.

### `API_INTEGRATION`
**Required.** The name of an API Integration object (`CREATE API INTEGRATION`) that defines the cloud provider, authentication method, and allowed URL prefixes for the proxy service. The calling role must have `USAGE` on this integration.

### `HEADERS`
Optional. Custom HTTP headers sent with every request to the proxy. Format: `'header-name' = 'header-value'`. Header names must consist of visible ASCII characters (codes 32–126) excluding: space, `(`, `)`, `,`, `/`, `:`, `;`, `<`, `>`, `=`, `"`, `?`, `@`, `[`, `]`, `\`, `{`, `}`. Snowflake prepends `sf-custom-` to all header names. Total header value size must not exceed 8 KB.

### `CONTEXT_HEADERS`
Optional. Snowflake context function values sent as additional HTTP headers. Snowflake prepends `sf-context-` to the header name. Supported context functions include (non-exhaustive):
`CURRENT_ACCOUNT()`, `CURRENT_USER()`, `CURRENT_ROLE()`, `CURRENT_TIMESTAMP()`, `CURRENT_DATABASE()`, `CURRENT_SCHEMA()`, `CURRENT_WAREHOUSE()`, and others listed in Snowflake documentation.

### `MAX_BATCH_ROWS`
Optional. Maximum number of rows Snowflake includes in a single HTTP POST batch to the remote service. Default: Snowflake auto-estimates based on row size. Set explicitly when the remote service enforces a documented row-per-request limit (e.g., some APIs accept at most 100 rows per call).

### `COMPRESSION`
Controls compression of the JSON request payload. Valid values:
- `AUTO` (default): Snowflake compresses with GZIP when beneficial; falls back to uncompressed.
- `GZIP`: always compress.
- `DEFLATE`: compress with DEFLATE.
- `NONE`: always send uncompressed. Recommended during development for payload inspection.

### `REQUEST_TRANSLATOR`
Optional. Name of a scalar JavaScript UDF that receives Snowflake's standard row-array JSON envelope and returns a transformed JSON object. Use when the remote API expects a custom request schema that differs from Snowflake's default format.

### `RESPONSE_TRANSLATOR`
Optional. Name of a scalar JavaScript UDF that receives the raw HTTP response body and returns a Snowflake-compatible row-array JSON envelope. Use when the remote API returns a custom response schema.

### `AS '<url_of_proxy_and_resource>'`
**Required.** The HTTPS URL of the proxy service endpoint. Snowflake sends HTTP POST requests to this URL. The URL must match one of the allowed URL prefixes configured in the `API_INTEGRATION` object. This URL identifies both the proxy (API Gateway, Azure API Management, etc.) and the specific resource/route.

---

## Snowflake Request/Response Envelope

**Request body** (default, before any REQUEST_TRANSLATOR):

```json
{
  "data": [
    [0, arg1_value, arg2_value, ...],
    [1, arg1_value, arg2_value, ...],
    ...
  ]
}
```

**Expected response body** (default, before any RESPONSE_TRANSLATOR):

```json
{
  "data": [
    [0, result_value],
    [1, result_value],
    ...
  ]
}
```

Row indices in the response must match the request row indices.

---

## Usage Notes

- External functions are synchronous: Snowflake waits for the HTTP response before returning results.
- The remote service must be accessible via an API Gateway (AWS API Gateway, Azure API Management, or Google Cloud API Gateway) configured in the API Integration.
- `IF NOT EXISTS` is **not supported** for external functions. Use `OR REPLACE` for idempotent creation, or wrap in a `SHOW EXTERNAL FUNCTIONS` check.
- Header values are transmitted in plaintext to the proxy; use `SECRETS` (via `EXTERNAL_ACCESS_INTEGRATIONS`) for credentials rather than embedding them in `HEADERS`.
