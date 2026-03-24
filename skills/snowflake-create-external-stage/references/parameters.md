# Snowflake CREATE STAGE (External) — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] STAGE [ IF NOT EXISTS ] <external_stage_name>
    URL = '<cloud_specific_url>'
    [ STORAGE_INTEGRATION = <integration_name> ]
    [ CREDENTIALS = ( <cloud_credentials> ) ]
    [ ENCRYPTION = ( <cloud_encryption> ) ]
    [ DIRECTORY = (
        ENABLE = { TRUE | FALSE }
        [ REFRESH_ON_CREATE = { TRUE | FALSE } ]
        [ AUTO_REFRESH = { TRUE | FALSE } ]
        [ NOTIFICATION_INTEGRATION = '<integration_name>' ]
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

### Amazon S3 Credentials

```sql
-- Preferred: storage integration (no secrets in DDL)
STORAGE_INTEGRATION = <integration_name>

-- Alternative: IAM role
CREDENTIALS = ( AWS_ROLE = '<iam_role_arn>' )

-- Alternative: access key (not recommended for production)
CREDENTIALS = (
    AWS_KEY_ID = '<access_key_id>'
    AWS_SECRET_KEY = '<secret_access_key>'
    [ AWS_TOKEN = '<temporary_token>' ]
)
```

### Amazon S3 Encryption

```sql
ENCRYPTION = ( TYPE = 'AWS_CSE' MASTER_KEY = '<base64_master_key>' )
ENCRYPTION = ( TYPE = 'AWS_SSE_S3' )
ENCRYPTION = ( TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<kms_key_arn>' ] )
ENCRYPTION = ( TYPE = 'NONE' )
```

### Google Cloud Storage Credentials

```sql
-- GCS requires a storage integration; direct credentials are not supported
STORAGE_INTEGRATION = <integration_name>
```

### Google Cloud Storage Encryption

```sql
ENCRYPTION = ( TYPE = 'GCS_SSE_KMS' [ KMS_KEY_ID = '<kms_key_id>' ] )
ENCRYPTION = ( TYPE = 'NONE' )
```

### Microsoft Azure Credentials

```sql
-- Preferred: storage integration
STORAGE_INTEGRATION = <integration_name>

-- Alternative: SAS token
CREDENTIALS = ( AZURE_SAS_TOKEN = '<sas_token>' )
```

### Microsoft Azure Encryption

```sql
ENCRYPTION = ( TYPE = 'AZURE_CSE' MASTER_KEY = '<base64_master_key>' )
ENCRYPTION = ( TYPE = 'NONE' )
```

---

## URL Formats by Cloud Provider

| Provider | URL Format | Example |
|---|---|---|
| Amazon S3 | `s3://<bucket>[/<path>/]` | `s3://my-bucket/data/` |
| Amazon S3 Gov | `s3gov://<bucket>[/<path>/]` | `s3gov://my-gov-bucket/` |
| S3-Compatible | `s3compat://<bucket>[/<path>/]` | `s3compat://my-bucket/` |
| Google Cloud Storage | `gcs://<bucket>[/<path>/]` | `gcs://my-bucket/data/` |
| Microsoft Azure Blob | `azure://<account>.blob.core.windows.net/<container>[/<path>/]` | `azure://myaccount.blob.core.windows.net/mycontainer/` |
| Microsoft Azure ADLS | `azure://<account>.dfs.core.windows.net/<container>[/<path>/]` | `azure://myaccount.dfs.core.windows.net/mycontainer/` |
| Microsoft OneLake | `azure://onelake.blob.fabric.microsoft.com/<workspace_id>/<item_id>/Files[/<path>/]` | — |

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| `TEMP / TEMPORARY` | false | Stage is dropped at end of session when true |
| `IF NOT EXISTS` | — | Prevents error if stage already exists |
| `URL` | **Required** | Cloud storage path |
| `STORAGE_INTEGRATION` | none | Recommended over CREDENTIALS |
| `CREDENTIALS` | none | Inline cloud credentials; mutually exclusive with STORAGE_INTEGRATION |
| `ENCRYPTION TYPE` | none (provider default) | See per-provider options above |
| `DIRECTORY ENABLE` | FALSE | Enables directory table for file browsing |
| `DIRECTORY REFRESH_ON_CREATE` | TRUE | Automatically refreshes directory on stage creation |
| `DIRECTORY AUTO_REFRESH` | FALSE | Automatically refreshes directory when files are added |
| `DIRECTORY NOTIFICATION_INTEGRATION` | none | Required for AUTO_REFRESH on GCS and Azure |
| `FILE_FORMAT TYPE` | CSV | Format used when loading/unloading without explicit format |
| `COMMENT` | none | Free-text description |

---

## Detailed Parameter Descriptions

### URL
- **Required** for all external stages.
- Points to the root of the cloud storage location where files reside.
- Snowflake limits access to the path specified and its sub-paths.

### STORAGE_INTEGRATION = `<integration_name>`
- Delegates authentication to a Snowflake-managed IAM entity; no secrets are stored in the stage definition.
- Must be created separately with `CREATE STORAGE INTEGRATION`.
- Mutually exclusive with `CREDENTIALS`.
- Strongly preferred over inline credentials for security and auditability.

### CREDENTIALS
- Embed cloud provider credentials directly in the stage.
- **S3**: `AWS_KEY_ID` + `AWS_SECRET_KEY` (+ optional `AWS_TOKEN` for temporary credentials), or `AWS_ROLE` for IAM role assumption.
- **Azure**: `AZURE_SAS_TOKEN`.
- **GCS**: Not supported; use `STORAGE_INTEGRATION`.
- Avoid in production — prefer STORAGE_INTEGRATION.

### ENCRYPTION
- Specifies the client-side or server-side encryption method for files in the stage.
- **AWS_CSE**: Client-side encryption using a customer-provided master key (`MASTER_KEY`).
- **AWS_SSE_S3**: Server-side encryption with S3-managed keys (no additional config needed).
- **AWS_SSE_KMS**: Server-side encryption with AWS KMS; optionally specify `KMS_KEY_ID`.
- **GCS_SSE_KMS**: Server-side encryption with Google Cloud KMS; optionally specify `KMS_KEY_ID`.
- **AZURE_CSE**: Client-side encryption with a customer-provided master key (`MASTER_KEY`).
- **NONE**: No encryption.

### DIRECTORY
- Creates a directory table that catalogs files in the stage, enabling `LIST @stage` and `SELECT * FROM DIRECTORY(@stage)` queries.
- `ENABLE = TRUE` activates the directory table.
- `REFRESH_ON_CREATE = TRUE` (default) populates the directory immediately on stage creation; set to FALSE to skip the initial refresh.
- `AUTO_REFRESH = TRUE` keeps the directory up to date automatically via cloud event notifications (requires a `NOTIFICATION_INTEGRATION` for GCS and Azure).
- `NOTIFICATION_INTEGRATION` — name of a notification integration configured for the cloud provider (required for GCS and Azure auto-refresh).

### FILE_FORMAT
- Defines the default format for COPY INTO operations on this stage.
- Can reference a named format: `FORMAT_NAME = 'my_csv_format'`.
- Or specify inline: `TYPE = CSV [ formatTypeOptions ]`.
- See the `snowflake-create-file-format` skill for full format type option details.

### TEMP / TEMPORARY
- Stage is automatically dropped at the end of the current session.
- Useful for one-off load operations.

### COMMENT = `'<string>'`
- Free-text description visible in `SHOW STAGES` and Snowsight.

### TAG
- Key-value metadata tags for governance and cost attribution.
- Example: `TAG (environment = 'prod', team = 'data-engineering')`.

---

## Access Control Requirements

- `CREATE STAGE` privilege on the target schema.
- `USAGE` privilege on the storage integration (if using `STORAGE_INTEGRATION`).
- The Snowflake IAM entity (from the storage integration) must have read/write permissions on the cloud storage bucket/container.
