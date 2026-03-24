# Snowflake CREATE EXTERNAL VOLUME — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] EXTERNAL VOLUME [ IF NOT EXISTS ]
    <name>
    STORAGE_LOCATIONS =
      (
        (
          NAME = '<storage_location_name>'
          STORAGE_PROVIDER = '{ S3 | S3GOV | S3COMPAT | GCS | AZURE }'
          STORAGE_BASE_URL = '<protocol>://<bucket_or_container>[/<path>/]'
          { cloudProviderParams }
        )
        [ , ( ... ) , ... ]
      )
    [ ALLOW_WRITES = { TRUE | FALSE } ]
    [ COMMENT = '<string_literal>' ]
```

### Amazon S3 / S3GOV (cloudProviderParams)

```sql
STORAGE_PROVIDER = '{ S3 | S3GOV }'
STORAGE_AWS_ROLE_ARN = '<iam_role_arn>'
STORAGE_BASE_URL = '{ s3:// | s3gov:// }<bucket>[/<path>/]'
[ STORAGE_AWS_ACCESS_POINT_ARN = '<access_point_arn>' ]
[ STORAGE_AWS_EXTERNAL_ID = '<external_id>' ]
[ ENCRYPTION = (
    [ TYPE = 'AWS_SSE_S3' ]
  | [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<kms_key_arn>' ] ]
  | [ TYPE = 'NONE' ]
  ) ]
[ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
```

### S3-Compatible Storage (cloudProviderParams)

```sql
STORAGE_PROVIDER = 'S3COMPAT'
STORAGE_BASE_URL = 's3compat://<bucket>[/<path>/]'
CREDENTIALS = ( AWS_KEY_ID = '<key>' AWS_SECRET_KEY = '<secret>' )
STORAGE_ENDPOINT = '<s3_api_compatible_endpoint>'
```

### Google Cloud Storage (cloudProviderParams)

```sql
STORAGE_PROVIDER = 'GCS'
STORAGE_BASE_URL = 'gcs://<bucket>[/<path>/]'
[ ENCRYPTION = (
    [ TYPE = 'GCS_SSE_KMS' [ KMS_KEY_ID = '<kms_key_id>' ] ]
  | [ TYPE = 'NONE' ]
  ) ]
```

### Microsoft Azure (cloudProviderParams)

```sql
STORAGE_PROVIDER = 'AZURE'
AZURE_TENANT_ID = '<tenant_id>'
STORAGE_BASE_URL = 'azure://<account>.{ blob | dfs }.core.windows.net/<container>[/<path>/]'
[ USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } ]
```

Azure Fabric OneLake:

```sql
STORAGE_BASE_URL = 'azure://[<region>-]onelake.{ dfs | blob }.fabric.microsoft.com/<workspace>/<lakehouse>/<path>/'
```

---

## Top-Level Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| `IF NOT EXISTS` | — | Prevents error if volume already exists |
| `<name>` | **Required** | Unique identifier within the account |
| `STORAGE_LOCATIONS` | **Required** | At least one storage location must be defined |
| `ALLOW_WRITES` | TRUE | Enables write operations for Iceberg tables using Snowflake catalog |
| `COMMENT` | none | Free-text description |

---

## Storage Location Parameter Defaults

| Parameter | Default | Required | Notes |
|---|---|---|---|
| `NAME` | **Required** | yes | Unique label for this storage location within the volume |
| `STORAGE_PROVIDER` | **Required** | yes | S3, S3GOV, S3COMPAT, GCS, or AZURE |
| `STORAGE_BASE_URL` | **Required** | yes | Cloud storage path with provider-specific protocol |
| `STORAGE_AWS_ROLE_ARN` | **Required for S3/S3GOV** | yes (S3) | IAM role ARN granting access to S3 bucket |
| `STORAGE_AWS_ACCESS_POINT_ARN` | none | no | S3 access point ARN for VPC-only access |
| `STORAGE_AWS_EXTERNAL_ID` | auto-generated | no | External ID for cross-account role assumption |
| `AZURE_TENANT_ID` | **Required for AZURE** | yes (Azure) | Azure Active Directory tenant ID |
| `CREDENTIALS` | **Required for S3COMPAT** | yes (S3Compat) | AWS_KEY_ID + AWS_SECRET_KEY |
| `STORAGE_ENDPOINT` | **Required for S3COMPAT** | yes (S3Compat) | S3-compatible API endpoint hostname |
| `ENCRYPTION TYPE` | none (provider default) | no | See per-provider encryption options |
| `USE_PRIVATELINK_ENDPOINT` | FALSE | no | Route traffic through PrivateLink (S3, Azure) |

---

## Detailed Parameter Descriptions

### `<name>`
- Unique identifier for the external volume within the Snowflake account.
- Must start with an alphabetic character; may contain letters, digits, and underscores.
- Referenceable from Iceberg table definitions via `EXTERNAL_VOLUME = '<name>'`.

### STORAGE_LOCATIONS
- Required list of one or more named cloud storage locations.
- Multiple locations can span different cloud providers, regions, or accounts.
- Snowflake selects the appropriate location based on the Snowflake account region.
- Each location must have a unique `NAME` within the volume.

### STORAGE_PROVIDER
- Identifies the cloud storage platform.
- `S3` — Amazon S3 (commercial regions).
- `S3GOV` — Amazon S3 (US government regions).
- `S3COMPAT` — Any S3-compatible object store (MinIO, Cloudflare R2, etc.).
- `GCS` — Google Cloud Storage.
- `AZURE` — Microsoft Azure Blob Storage or Azure Data Lake Storage Gen2.

### STORAGE_BASE_URL
- The root URL of the storage location. All Iceberg data must reside at or below this path.
- Protocol must match the `STORAGE_PROVIDER`.
- S3 bucket names with dots (`.`) are not supported.

### STORAGE_AWS_ROLE_ARN
- ARN of the AWS IAM role that Snowflake assumes to access the S3 bucket.
- The IAM role trust policy must allow Snowflake's service principal to assume it.
- Required for S3 and S3GOV; not used for S3COMPAT.

### STORAGE_AWS_EXTERNAL_ID
- Optional override for the external ID in the IAM role trust policy.
- If not specified, Snowflake auto-generates one; retrieve it via `DESCRIBE EXTERNAL VOLUME`.

### STORAGE_AWS_ACCESS_POINT_ARN
- ARN of an S3 access point configured to restrict bucket access to a specific VPC.
- Use when S3 bucket policies enforce access point usage.

### AZURE_TENANT_ID
- The Azure Active Directory (AAD) tenant ID of the Azure subscription containing the storage account.
- Required for all Azure storage locations.

### ENCRYPTION (S3/S3GOV)
- `AWS_SSE_S3` — Server-side encryption with S3-managed keys. No additional parameters.
- `AWS_SSE_KMS` — Server-side encryption with AWS KMS. Optionally specify `KMS_KEY_ID` for a customer-managed key; omit to use the AWS-managed KMS key.
- `NONE` — No encryption enforced by Snowflake (bucket-level encryption may still apply).

### ENCRYPTION (GCS)
- `GCS_SSE_KMS` — Server-side encryption with Google Cloud KMS. Optionally specify `KMS_KEY_ID`.
- `NONE` — No encryption enforced by Snowflake.

### USE_PRIVATELINK_ENDPOINT
- When TRUE, Snowflake routes storage traffic through a configured PrivateLink endpoint (S3 or Azure).
- Requires the Snowflake account to be configured with the appropriate PrivateLink.
- Default: FALSE.

### ALLOW_WRITES
- When TRUE (default), Snowflake-managed Iceberg tables can write Parquet data and metadata to this volume.
- Set to FALSE for read-only volumes (e.g., accessing data managed by an external engine).

### COMMENT
- Free-text description visible in `SHOW EXTERNAL VOLUMES` and Snowsight.

---

## Important Constraints

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- An external volume that has associated Iceberg tables cannot be dropped or replaced without first dropping those tables.
- S3 bucket names containing dots are not supported.
- All Parquet data files and Iceberg metadata files must reside within `STORAGE_BASE_URL`.
- After creating the external volume, retrieve the Snowflake IAM principal via `DESCRIBE EXTERNAL VOLUME <name>` and configure the corresponding trust/permissions in your cloud provider.

---

## Access Control Requirements

- `CREATE EXTERNAL VOLUME` privilege (typically granted to ACCOUNTADMIN or a custom role).
- `USAGE` privilege on the external volume to reference it from Iceberg tables.
- Cloud provider IAM permissions must be configured separately after volume creation.
