# CREATE PROCEDURE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-procedure

## Full Syntax

### Snowflake Scripting (SQL) — most common
```sql
CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] [, ...] ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [, ...] ] ) }
  LANGUAGE SQL
  [ { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT } ]
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
AS
  '<procedure_body>'
```

### JavaScript
```sql
CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] [, ...] ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [, ...] ] ) }
  LANGUAGE JAVASCRIPT
  [ { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT } ]
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
AS
  '<procedure_body>'
```

### Python
```sql
CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] [, ...] ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [, ...] ] ) }
  LANGUAGE PYTHON
  RUNTIME_VERSION = '<version>'
  PACKAGES = ( '<package_name>' [, ...] )
  HANDLER = '<function_name>'
  [ IMPORTS = ( '<stage_path_and_file>' [, ...] ) ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name> [, ...] ) ]
  [ SECRETS = ( '<variable>' = <secret_name> [, ...] ) ]
  [ { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT } ]
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
AS
  '<procedure_body>'
```

### Java
```sql
CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] [, ...] ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [, ...] ] ) }
  LANGUAGE JAVA
  RUNTIME_VERSION = '<version>'
  PACKAGES = ( 'com.snowflake:snowpark:<version>' [, ...] )
  HANDLER = '<fully_qualified_method_name>'
  [ IMPORTS = ( '<stage_path_and_file>' [, ...] ) ]
  [ TARGET_PATH = '<stage_path_and_file>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name> [, ...] ) ]
  [ SECRETS = ( '<variable>' = <secret_name> [, ...] ) ]
  [ { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT } ]
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
AS
  '<procedure_body>'
```

### Scala
```sql
CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE [ IF NOT EXISTS ]
  <name> ( [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] [, ...] ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [, ...] ] ) }
  LANGUAGE SCALA
  RUNTIME_VERSION = '<version>'
  PACKAGES = ( 'com.snowflake:snowpark:<version>' [, ...] )
  HANDLER = '<fully_qualified_method_name>'
  [ IMPORTS = ( '<stage_path_and_file>' [, ...] ) ]
  [ TARGET_PATH = '<stage_path_and_file>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name> [, ...] ) ]
  [ SECRETS = ( '<variable>' = <secret_name> [, ...] ) ]
  [ { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT } ]
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
AS
  '<procedure_body>'
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| `SECURE` | (not set — procedure is not secure) |
| `TEMP / TEMPORARY` | (not set — permanent procedure) |
| `LANGUAGE` | `SQL` |
| `RUNTIME_VERSION` | (required for Java/Python/Scala) |
| `NULL handling` | `CALLED ON NULL INPUT` |
| `EXECUTE AS` | `OWNER` |
| `COPY GRANTS` | (not set) |
| `COMMENT` | (none) |
| `IMPORTS` | (none) |
| `TARGET_PATH` | (none — auto-generated for Java/Scala) |
| `EXTERNAL_ACCESS_INTEGRATIONS` | (none) |
| `SECRETS` | (none) |

## Parameter Descriptions

### `<name>` *(required)*
Unique identifier for the procedure. Procedures support **overloading**: two procedures may share the same name if they differ in argument count or argument data types.

### `( <arg_name> <arg_data_type> [DEFAULT <default_value>] [, ...] )` *(required)*
Argument list. Arguments with `DEFAULT` values are optional at call time. Arguments without defaults are positional and required. Snowflake SQL data types are used (e.g., `VARCHAR`, `NUMBER`, `VARIANT`).

### `RETURNS` *(required)*
Specifies the return type:
- `<result_data_type>`: A scalar Snowflake SQL type.
- `TABLE ( <col_name> <col_data_type> [, ...] )`: A tabular result set.
- Append `NOT NULL` to forbid NULL returns; `NULL` (default) allows NULL.

### `LANGUAGE` *(required)*
Handler language. Valid values: `SQL`, `JAVASCRIPT`, `PYTHON`, `JAVA`, `SCALA`.
Default: `SQL`.

### `RUNTIME_VERSION = '<version>'` *(required for Python, Java, Scala)*
- Python: `'3.10'`, `'3.11'`, `'3.12'`, `'3.13'`
- Java: `'11'`
- Scala: `'2.12'`, `'2.13'`

### `PACKAGES = ( '<package_name>' [, ...] )` *(required for Python, Java, Scala)*
Anaconda or Snowflake channel packages for Python; Maven coordinates for Java/Scala.
Java/Scala must include `'com.snowflake:snowpark:<version>'`.

### `HANDLER = '<handler>'` *(required for Python, Java, Scala)*
- Python inline: function name (e.g., `'my_func'`)
- Python staged: `'module.function'`
- Java/Scala: fully qualified method name (e.g., `'com.example.MyClass.myMethod'`)

### `SECURE`
When set, hides the procedure body from users who do not own or have the OWNERSHIP privilege. Prevents data exfiltration through procedure introspection.

### `TEMP | TEMPORARY`
The procedure exists only for the duration of the current session and is automatically dropped on session close.

### `CALLED ON NULL INPUT` (default)
The procedure is called even when one or more arguments are NULL. The handler is responsible for null handling.

### `RETURNS NULL ON NULL INPUT` / `STRICT`
If any argument is NULL, the procedure returns NULL immediately without invoking the handler.

### `COMMENT = '<string_literal>'`
Free-text description. Visible in `SHOW PROCEDURES` and the Snowsight UI.

### `EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER }`
- `OWNER` (default): Runs with the privileges of the procedure owner role. The caller need not have access to underlying objects.
- `CALLER`: Runs with the privileges of the calling role. The caller must have direct access to all referenced objects.
- `RESTRICTED CALLER`: Like CALLER, but with additional restrictions on privilege escalation.

### `COPY GRANTS`
Preserves existing privilege grants when using `CREATE OR REPLACE PROCEDURE`. Without this, all grants are revoked on replacement.

### `IMPORTS = ( '<stage_path_and_file>' [, ...] )`
External files (JARs, Python modules, resource files) made available to the handler at runtime. Reference a `@stage/path/file` location.

### `TARGET_PATH = '<stage_path_and_file>'` *(Java/Scala only)*
Destination path where Snowflake writes the compiled JAR file. If omitted, a path is auto-generated.

### `EXTERNAL_ACCESS_INTEGRATIONS = ( <name> [, ...] )`
Named external access integrations allowing the procedure to make outbound network calls.

### `SECRETS = ( '<variable>' = <secret_name> [, ...] )`
Maps Snowflake Secret objects to named variables accessible within the handler code.

### `AS '<procedure_body>'`
The handler source code. For staged handlers (Java/Scala/Python), omit this clause and specify the stage location in `IMPORTS`.

## Key Behavioral Notes

- `CREATE OR REPLACE` is atomic: the old procedure is deleted and the new one created in a single transaction.
- Stored procedures are **not** atomic internally: a statement failure mid-procedure does not automatically roll back prior statements. Use explicit `BEGIN … COMMIT / ROLLBACK` blocks when transactional integrity is required.
- Overloaded procedures must differ in argument count or argument data types; return type alone is not sufficient to distinguish overloads.
- `IF NOT EXISTS` and `OR REPLACE` are mutually exclusive.
