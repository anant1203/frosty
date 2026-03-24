---
name: snowflake-create-external-stage
description: Consult Snowflake CREATE STAGE parameter reference before generating any CREATE STAGE DDL for external stages.
---

Before writing a CREATE STAGE statement for an external stage:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE STAGE IF NOT EXISTS`.
5. Always include the required `URL` parameter for external stages pointing to the correct cloud storage path (s3://, gcs://, or azure://).
6. Prefer `STORAGE_INTEGRATION` over inline `CREDENTIALS` for authentication — it is more secure and avoids embedding secrets in DDL.
7. If the user provides raw credentials (AWS keys, SAS tokens), emit them but add a comment recommending migration to a storage integration.
8. Choose the encryption type appropriate to the cloud provider (AWS_SSE_S3, AWS_SSE_KMS, GCS_SSE_KMS, AZURE_CSE, etc.) only if the user explicitly requests encryption configuration.
9. Enable the DIRECTORY table only when the user needs to query staged files via directory table functions.
