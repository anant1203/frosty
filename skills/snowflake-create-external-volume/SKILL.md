---
name: snowflake-create-external-volume
description: Consult Snowflake CREATE EXTERNAL VOLUME parameter reference before generating any CREATE EXTERNAL VOLUME DDL.
---

Before writing a CREATE EXTERNAL VOLUME statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE EXTERNAL VOLUME IF NOT EXISTS`.
5. `STORAGE_LOCATIONS` is required and must contain at least one named location; always ask for or infer the cloud provider, bucket/container URL, and authentication details.
6. For S3, always include `STORAGE_AWS_ROLE_ARN`; never embed raw AWS access keys in external volume definitions.
7. For Azure, always include `AZURE_TENANT_ID` alongside the `STORAGE_BASE_URL`.
8. `ALLOW_WRITES` defaults to TRUE — set it to FALSE explicitly only when the volume is intended to be read-only (e.g., for read-only Iceberg catalog integrations).
9. Do not combine `OR REPLACE` and `IF NOT EXISTS` in the same statement — they are mutually exclusive.
