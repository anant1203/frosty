# CREATE NOTEBOOK — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-notebook

---

## Full Syntax

```sql
CREATE [ OR REPLACE ] NOTEBOOK [ IF NOT EXISTS ] <name>
  [ FROM '<source_location>' ]
  [ MAIN_FILE = '<main_file_name>' ]
  [ COMMENT = '<string_literal>' ]
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ IDLE_AUTO_SHUTDOWN_TIME_SECONDS = <number_of_seconds> ]
  [ RUNTIME_NAME = '<runtime_name>' ]
  [ COMPUTE_POOL = '<compute_pool_name>' ]
  [ WAREHOUSE = <warehouse_name> ]
```

---

## Defaults Table

| Parameter | Default Value |
|-----------|---------------|
| `FROM` | — (creates a blank template notebook) |
| `MAIN_FILE` | — (none; required when `FROM` is specified) |
| `COMMENT` | — (none) |
| `QUERY_WAREHOUSE` | — (none; required for `EXECUTE NOTEBOOK`) |
| `IDLE_AUTO_SHUTDOWN_TIME_SECONDS` | `3600` (Container Runtime only) |
| `RUNTIME_NAME` | `'SYSTEM$WAREHOUSE_RUNTIME'` |
| `COMPUTE_POOL` | — (none; required for Container Runtime) |
| `WAREHOUSE` | `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE` (account default) |

---

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the notebook within its schema. Must start with an alphabetic character. If the name contains special characters or spaces it must be enclosed in double quotes.

---

### `FROM '<source_location>'`
A stage URI pointing to the directory or `.ipynb` file to import. When specified, `MAIN_FILE` must also be provided to identify which file is the entry point.

**Valid values:** Any valid Snowflake internal or external stage URI (e.g. `'@my_stage/notebooks/'`).
**Default:** Omitting `FROM` creates a new blank notebook from the built-in template.

---

### `MAIN_FILE = '<main_file_name>'`
The name of the `.ipynb` file (within the location specified by `FROM`) that acts as the notebook's entry point.

**Valid values:** A filename string ending in `.ipynb`.
**Default:** None. Must be provided whenever `FROM` is used.

---

### `COMMENT = '<string_literal>'`
A free-text description attached to the notebook object. Visible in `SHOW NOTEBOOKS` and the Snowflake UI.

**Valid values:** Any string literal.
**Default:** None.

---

### `QUERY_WAREHOUSE = <warehouse_name>`
The virtual warehouse used to execute SQL cells and to run the notebook when called via `EXECUTE NOTEBOOK`. This is separate from the Python compute warehouse.

**Valid values:** Name of an existing warehouse in the same account.
**Default:** None. **Required** when the notebook will be invoked with `EXECUTE NOTEBOOK`.

---

### `IDLE_AUTO_SHUTDOWN_TIME_SECONDS = <number_of_seconds>`
Applies to **Container Runtime notebooks only**. The number of seconds of idle time after which the container is automatically shut down to save compute costs.

**Valid values:** Integer between `60` and `259200` (72 hours).
**Default:** `3600` (1 hour).
**Note:** This parameter has no effect on Warehouse Runtime (`SYSTEM$WAREHOUSE_RUNTIME`) notebooks.

---

### `RUNTIME_NAME = '<runtime_name>'`
Specifies the execution environment for the notebook.

| Value | Description |
|-------|-------------|
| `'SYSTEM$WAREHOUSE_RUNTIME'` | (Default) Runs on a Snowflake virtual warehouse; standard Python + SQL. |
| `'SYSTEM$BASIC_RUNTIME'` | Container-based runtime with a CPU compute pool; supports additional Python packages. |
| `'SYSTEM$GPU_RUNTIME'` | Container-based runtime with a GPU compute pool; for ML/AI workloads. |

**Default:** `'SYSTEM$WAREHOUSE_RUNTIME'`

When using `'SYSTEM$BASIC_RUNTIME'` or `'SYSTEM$GPU_RUNTIME'`, `COMPUTE_POOL` must also be specified.

---

### `COMPUTE_POOL = '<compute_pool_name>'`
The name of the Snowpark Container Services compute pool that hosts the notebook when using a Container Runtime (`SYSTEM$BASIC_RUNTIME` or `'SYSTEM$GPU_RUNTIME'`).

**Valid values:** Name of an existing compute pool in the same account.
**Default:** None. **Required** when `RUNTIME_NAME` is set to a Container Runtime value.
**Note:** Not applicable to `SYSTEM$WAREHOUSE_RUNTIME` notebooks.

---

### `EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] )`
A list of External Access Integration objects that grant the notebook network access to external endpoints (e.g. PyPI, external APIs). Used primarily with Container Runtime notebooks.

**Valid values:** One or more names of existing External Access Integration objects.
**Default:** None (no external network access).

---

### `WAREHOUSE = <warehouse_name>`
The virtual warehouse used to execute Python-based SQL queries and Snowpark operations inside the notebook (distinct from `QUERY_WAREHOUSE` which governs `EXECUTE NOTEBOOK` invocations).

**Valid values:** Name of an existing warehouse.
**Default:** The account-level default Streamlit/notebook warehouse (`DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE`).
