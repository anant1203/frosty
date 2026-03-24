---
name: snowflake-create-pipe
description: Consult Snowflake CREATE PIPE parameter reference before generating any CREATE PIPE DDL.
---

Before writing a CREATE PIPE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE PIPE IF NOT EXISTS`.
5. The `AS <copy_statement>` clause is required; always generate a valid `COPY INTO <table> FROM @<stage>` statement as part of the pipe definition.
6. `AUTO_INGEST = TRUE` is required for fully automated Snowpipe ingestion from external stages; it requires cloud event notification setup (SQS for S3, Pub/Sub for GCS, Azure Event Grid for Azure).
7. For S3 auto-ingest, include `AWS_SNS_TOPIC` with the ARN of the SNS topic configured on the source bucket.
8. For GCS or Azure auto-ingest, include `INTEGRATION` referencing a notification integration.
9. `ERROR_INTEGRATION` is optional but recommended for production pipelines to route load errors to a notification channel.
10. Do not combine `OR REPLACE` and `IF NOT EXISTS` in the same statement — they are mutually exclusive.
