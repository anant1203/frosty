# Snowflake CREATE PIPE — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] PIPE [ IF NOT EXISTS ] <name>
    [ AUTO_INGEST = { TRUE | FALSE } ]
    [ ERROR_INTEGRATION = <integration_name> ]
    [ AWS_SNS_TOPIC = '<sns_topic_arn>' ]
    [ INTEGRATION = '<notification_integration_name>' ]
    [ COMMENT = '<string_literal>' ]
    AS <copy_statement>
```

Where `<copy_statement>` is:

```sql
COPY INTO <table_name>
  FROM { @<stage_name>[/<path>] | ( SELECT ... FROM @<stage_name> ) }
  [ FILES = ( '<file_name>' [ , '<file_name>' ... ] ) ]
  [ PATTERN = '<regex_pattern>' ]
  [ FILE_FORMAT = ( { FORMAT_NAME = '<format_name>' | TYPE = <format_type> [ formatTypeOptions ] } ) ]
  [ MATCH_BY_COLUMN_NAME = { CASE_SENSITIVE | CASE_INSENSITIVE | NONE } ]
  [ <copyOptions> ]
```

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| `IF NOT EXISTS` | — | Prevents error if pipe already exists |
| `AUTO_INGEST` | FALSE | Must be TRUE for event-driven Snowpipe |
| `ERROR_INTEGRATION` | none | Notification integration for load errors |
| `AWS_SNS_TOPIC` | none | Required for S3 auto-ingest |
| `INTEGRATION` | none | Required for GCS or Azure auto-ingest |
| `COMMENT` | none | Free-text description |
| `AS <copy_statement>` | **Required** | The COPY INTO statement that defines loading behavior |

---

## Detailed Parameter Descriptions

### `<name>`
- Unique identifier for the pipe within the schema.
- Must start with an alphabetic character; quoted identifiers allow special characters.
- Case-insensitive unless double-quoted.

### AUTO_INGEST = { TRUE | FALSE }

- **FALSE** (default): Manual mode. New files are not automatically detected. Load them by calling the Snowpipe REST API (`insertFiles`) or `ALTER PIPE ... REFRESH`.
- **TRUE**: Automatic mode. Snowflake subscribes to cloud storage event notifications and triggers loads automatically when new files arrive in the stage.
  - **S3**: Requires an SNS topic configured to send `s3:ObjectCreated:*` events; provide the ARN via `AWS_SNS_TOPIC`.
  - **GCS**: Requires a Pub/Sub-based notification integration; provide the name via `INTEGRATION`.
  - **Azure**: Requires an Event Grid-based notification integration; provide the name via `INTEGRATION`.

### ERROR_INTEGRATION = `<integration_name>`

- Name of a notification integration (type = QUEUE) configured to receive Snowpipe error notifications.
- When specified, Snowflake sends a message to the notification queue whenever a file fails to load.
- Must be created separately with `CREATE NOTIFICATION INTEGRATION`.
- Recommended for production pipelines to enable load failure alerting.

### AWS_SNS_TOPIC = `'<sns_topic_arn>'`

- ARN of the Amazon SNS topic that the S3 source bucket is configured to publish `ObjectCreated` events to.
- Required when `AUTO_INGEST = TRUE` and the stage points to an S3 bucket.
- Snowflake subscribes an SQS queue to this SNS topic automatically; retrieve the SQS ARN via `SHOW PIPES` to complete the SNS subscription.
- Not applicable for GCS or Azure stages.

### INTEGRATION = `'<notification_integration_name>'`

- Name of a notification integration that provides access to the GCS Pub/Sub subscription or Azure Event Grid queue.
- Required when `AUTO_INGEST = TRUE` and the stage points to GCS or Azure Blob Storage.
- Must be created separately with `CREATE NOTIFICATION INTEGRATION`.
- The value must be specified in **uppercase**.
- Not applicable for S3 stages (use `AWS_SNS_TOPIC` instead).

### AS `<copy_statement>`

- **Required.** Defines which stage to ingest from and which table to load into.
- The COPY INTO statement is immutable after pipe creation — use `CREATE OR REPLACE PIPE` (or drop and recreate) to change it.
- Best practices:
  - Reference a named file format (`FORMAT_NAME`) rather than inline format options for maintainability.
  - Use `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` when column order in source files may vary.
  - Include `PATTERN` to filter files by name regex (e.g., only `.csv.gz` files).
  - Do not use `CURRENT_DATE`, `CURRENT_TIMESTAMP`, or similar non-deterministic functions in the copy statement.

### COMMENT = `'<string>'`

- Free-text description displayed in `SHOW PIPES` and Snowsight.
- Useful for documenting the source system, target table, and owning team.

---

## Auto-Ingest Setup by Cloud Provider

| Cloud Provider | Stage URL Protocol | Parameter to Set | Setup Required in Cloud |
|---|---|---|---|
| Amazon S3 | `s3://` | `AWS_SNS_TOPIC = '<arn>'` | S3 → SNS notification for `ObjectCreated:*` events |
| Google Cloud Storage | `gcs://` | `INTEGRATION = '<name>'` | GCS → Pub/Sub notification; create NOTIFICATION INTEGRATION in Snowflake |
| Microsoft Azure | `azure://` | `INTEGRATION = '<name>'` | Azure Blob → Event Grid → Storage Queue; create NOTIFICATION INTEGRATION in Snowflake |

---

## Common COPY INTO Options (copyOptions)

| Option | Default | Description |
|---|---|---|
| `ON_ERROR` | ABORT_STATEMENT | Behavior on error: ABORT_STATEMENT, CONTINUE, SKIP_FILE, SKIP_FILE_n |
| `SIZE_LIMIT` | none | Max bytes to load in a single COPY execution |
| `PURGE` | FALSE | Delete staged files after successful load |
| `FORCE` | FALSE | Re-load already-loaded files |
| `TRUNCATECOLUMNS` | FALSE | Truncate string values that exceed column width instead of erroring |
| `LOAD_UNCERTAIN_FILES` | FALSE | Load files whose load status is unknown |

---

## Important Constraints

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- The COPY INTO statement in the pipe definition cannot be modified after creation — the pipe must be recreated.
- Snowpipe processes files **asynchronously**; there is no guarantee of ordering.
- Snowpipe does not re-load files that have already been successfully loaded (tracked via load history for 64 days).
- `AUTO_INGEST = TRUE` requires the stage to be an external stage; internal stages do not support cloud event notifications.

---

## Access Control Requirements

- `CREATE PIPE` privilege on the target schema.
- `USAGE` on the stage referenced in the COPY INTO statement.
- `INSERT` privilege on the target table.
- `USAGE` on the notification integration (if using `ERROR_INTEGRATION` or `INTEGRATION`).
- Snowpipe service user must have appropriate privileges to execute the COPY INTO statement at ingest time.

---

## Monitoring Pipes

```sql
-- View pipe status and pending file count
SELECT SYSTEM$PIPE_STATUS('<pipe_name>');

-- View load history
SELECT * FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => '<table_name>',
    START_TIME => DATEADD('hours', -24, CURRENT_TIMESTAMP())
));

-- Manual refresh (re-scan stage for new files)
ALTER PIPE <pipe_name> REFRESH;

-- Pause / resume auto-ingest
ALTER PIPE <pipe_name> SET PIPE_EXECUTION_PAUSED = TRUE;
ALTER PIPE <pipe_name> SET PIPE_EXECUTION_PAUSED = FALSE;
```
