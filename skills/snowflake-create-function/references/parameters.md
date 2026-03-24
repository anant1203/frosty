# CREATE FUNCTION — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-function

---

## Full Syntax

### General (language-agnostic skeleton)

```sql
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] FUNCTION [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE { SQL | JAVASCRIPT | PYTHON | JAVA | SCALA }
  [ { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ COMMENT = '<string_literal>' ]
  [ <language_specific_clauses> ]
  AS '<function_definition>'
```

### SQL UDF

```sql
CREATE [ OR REPLACE ] [ TEMP ] [ SECURE ] FUNCTION [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE SQL
  [ CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT ]
  [ VOLATILE | IMMUTABLE ]
  [ MEMOIZABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<sql_expression>'
```

### JavaScript UDF

```sql
CREATE [ OR REPLACE ] [ TEMP ] [ SECURE ] FUNCTION [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVASCRIPT
  [ CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<javascript_function_body>'
```

### Python UDF

```sql
CREATE [ OR REPLACE ] [ TEMP ] [ SECURE ] FUNCTION [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE PYTHON
  RUNTIME_VERSION = '<python_version>'
  [ AGGREGATE ]
  [ IMPORTS = ( '<stage_path_and_file_name>' [ , ... ] ) ]
  [ PACKAGES = ( '<package_name>[==<version>]' [ , ... ] ) ]
  [ ARTIFACT_REPOSITORY = '<repository_name>' ]
  HANDLER = '<function_name>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ SECRETS = ( '<variable_name>' = <secret_name> [ , ... ] ) ]
  [ CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<python_function_body>'
```

### Java UDF

```sql
CREATE [ OR REPLACE ] [ TEMP ] [ SECURE ] FUNCTION [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVA
  [ RUNTIME_VERSION = '<java_jdk_version>' ]
  [ IMPORTS = ( '<stage_path_and_file_name>' [ , ... ] ) ]
  [ PACKAGES = ( '<package_name:version>' [ , ... ] ) ]
  HANDLER = '<path_to_method>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ SECRETS = ( '<variable_name>' = <secret_name> [ , ... ] ) ]
  [ TARGET_PATH = '<stage_path_and_jar_name>' ]
  [ CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<java_code>'
```

### Scala UDF (Preview)

```sql
CREATE [ OR REPLACE ] [ TEMP ] [ SECURE ] FUNCTION [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS <result_data_type>
  [ [ NOT ] NULL ]
  LANGUAGE SCALA
  [ RUNTIME_VERSION = '<scala_version>' ]
  [ IMPORTS = ( '<stage_path_and_file_name>' [ , ... ] ) ]
  [ PACKAGES = ( '<package_name:version>' [ , ... ] ) ]
  HANDLER = '<path_to_method>'
  [ TARGET_PATH = '<stage_path_and_jar_name>' ]
  [ CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT ]
  [ VOLATILE | IMMUTABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<scala_code>'
```

---

## Defaults Table

| Parameter | Default Value |
|---|---|
| `OR REPLACE` | Not set (error if function already exists with same signature) |
| `TEMP / TEMPORARY` | Not set (permanent) |
| `SECURE` | Not set (definition visible to authorized users) |
| `IF NOT EXISTS` | Not set |
| `COPY GRANTS` | Not set |
| `NULL / NOT NULL` | `NULL` (function may return NULL) |
| `CALLED ON NULL INPUT` | `CALLED ON NULL INPUT` (function is invoked even if inputs are NULL) |
| `VOLATILE / IMMUTABLE` | `VOLATILE` |
| `COMMENT` | `'user-defined function'` |
| `RUNTIME_VERSION` (Java) | `'11'` |
| `RUNTIME_VERSION` (Scala) | `'2.12'` |
| `RUNTIME_VERSION` (Python) | No default — **required** |
| `HANDLER` | No default — **required** for Java, Scala, Python |
| `AGGREGATE` (Python) | Not set |
| `IMPORTS` | None |
| `PACKAGES` | None |
| `ARTIFACT_REPOSITORY` | None |
| `EXTERNAL_ACCESS_INTEGRATIONS` | None |
| `SECRETS` | None |
| `TARGET_PATH` | None (auto-generated path) |
| `MEMOIZABLE` (SQL) | Not set |

---

## Parameter Descriptions

### `name`
Identifier for the function. Function names need not be unique within a schema — Snowflake resolves calls by signature (name + argument data types). Use double-quoted identifiers for names containing special characters or that are case-sensitive.

### `arg_name arg_data_type`
Input argument name and its Snowflake SQL data type. Arguments with a `DEFAULT` value must appear after all required (non-default) arguments. All Snowflake SQL data types are supported except GEOGRAPHY for external functions.

### `DEFAULT default_value`
Specifies a literal or expression used when the caller omits that argument. Only supported for SQL and Python UDFs. Must be placed after all required arguments.

### `RETURNS result_data_type`
Scalar return type. Any Snowflake SQL data type is valid.

### `RETURNS TABLE (col_name col_data_type [, ...])`
Declares a tabular (UDTF) return. The function then returns a set of rows matching the column definitions. **Not supported for Scala.** The handler class must implement the process() / end_partition() pattern (Python/Java) or return a JavaScript array of objects.

### `OR REPLACE`
Atomically replaces an existing function with the same signature. Mutually exclusive with `IF NOT EXISTS`. Prefer `IF NOT EXISTS` in idempotent DDL scripts.

### `TEMP / TEMPORARY`
Creates a session-scoped function that is automatically dropped when the session ends.

### `SECURE`
Hides the function definition from non-owner roles. Use for functions that embed sensitive logic or proprietary algorithms.

### `IF NOT EXISTS`
Creates the function only when no function with the same signature exists in the schema. Mutually exclusive with `OR REPLACE`.

### `COPY GRANTS`
When used with `OR REPLACE`, preserves the existing privilege grants on the function being replaced.

### `NOT NULL`
Asserts that the function never returns NULL. Snowflake does not enforce this at runtime; it is informational.

### `LANGUAGE`
Specifies the handler language. Valid values: `SQL`, `JAVASCRIPT`, `PYTHON`, `JAVA`, `SCALA`.

### `CALLED ON NULL INPUT` (default)
The function is always called, even when one or more arguments are NULL. The function body is responsible for handling NULLs.

### `RETURNS NULL ON NULL INPUT` / `STRICT`
The function is not called when any argument is NULL; Snowflake returns NULL automatically. Equivalent aliases.

### `VOLATILE` (default)
Snowflake may re-evaluate the function for each row and does not cache results.

### `IMMUTABLE`
Declares that the function returns the same result for the same inputs within a single query. Snowflake may optimize by caching results. This is a hint — not enforced.

### `COMMENT`
Free-text description shown in `SHOW FUNCTIONS` and `DESCRIBE FUNCTION`. Default: `'user-defined function'`.

### `RUNTIME_VERSION` (Python)
**Required.** Python interpreter version. Supported values: `'3.9'`, `'3.10'`, `'3.11'`, `'3.12'`, `'3.13'`.

### `RUNTIME_VERSION` (Java)
JDK version. Supported values: `'11'` (default), `'17'`.

### `RUNTIME_VERSION` (Scala)
Scala compiler version. Supported values: `'2.12'` (default), `'2.13'` (preview).

### `HANDLER`
**Required for Java, Scala, Python.**
- Java/Scala scalar: `'ClassName.methodName'`
- Java/Scala tabular: `'ClassName'` (class implements the UDTF interface)
- Python: `'function_name'` or `'module.function_name'` for staged code

### `IMPORTS`
List of stage paths to JAR files (Java/Scala), Python `.py`/`.zip` files, or other resources. Format: `'@stage_name/path/to/file'`.

### `PACKAGES`
Anaconda or Maven package dependencies. Format for Python: `'package_name==version'` or `'package_name'`. Format for Java/Scala: `'group:artifact:version'`.

### `ARTIFACT_REPOSITORY` (Python)
Name of a custom artifact repository integration. Use when packages must be sourced from a private repository instead of Snowflake's Anaconda channel.

### `TARGET_PATH` (Java/Scala inline)
Stage location where Snowflake writes the compiled JAR for inline (non-staged) Java/Scala handlers.

### `EXTERNAL_ACCESS_INTEGRATIONS`
List of external access integrations that grant the function permission to make outbound network calls (e.g., to REST APIs). Requires the function to also use `SECRETS`.

### `SECRETS`
Key-value pairs mapping a variable name (accessible inside the handler via `_snowflake.get_generic_secret_string()`) to a secret object name.

### `MEMOIZABLE` (SQL only)
Enables result caching for scalar SQL UDFs that are called multiple times with the same arguments within a query. Not valid for other languages.

### `AGGREGATE` (Python, Preview)
Declares the Python UDF as an aggregate function (UDAF). The handler class must implement `__init__`, `accumulate`, `merge`, and `finish` methods.

### `AS 'function_definition'`
The body of the function. For SQL, a single SQL expression or SELECT statement. For JavaScript, the full JS function source. For Python/Java/Scala inline code, the source code as a string. Use `$$` as the delimiter to avoid escaping internal single quotes.
