---
name: snowflake-create-notification-integration
description: Consult Snowflake CREATE NOTIFICATION INTEGRATION parameter reference before generating any CREATE NOTIFICATION INTEGRATION DDL.
---

Before writing a CREATE NOTIFICATION INTEGRATION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested — do not bloat the DDL with unnecessary clauses.
4. Never use `CREATE OR REPLACE` — always use `CREATE NOTIFICATION INTEGRATION IF NOT EXISTS`.
5. Select the correct TYPE variant based on context: use `TYPE = EMAIL` for email notifications, `TYPE = WEBHOOK` for webhook integrations, and `TYPE = QUEUE` with the appropriate `NOTIFICATION_PROVIDER` (AWS_SNS, AZURE_EVENT_GRID, or GCP_PUBSUB) for cloud message-queue integrations.
6. Note that `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive — always prefer `IF NOT EXISTS`.
7. For QUEUE types, always include `DIRECTION = OUTBOUND` and the provider-specific ARN or endpoint parameters.
8. For WEBHOOK types, include `WEBHOOK_SECRET` whenever the URL requires authentication credentials.
