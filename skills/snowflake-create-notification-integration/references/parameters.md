# Snowflake CREATE NOTIFICATION INTEGRATION — Parameter Reference

## Syntax Variants

### TYPE = EMAIL

```sql
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  TYPE = EMAIL
  ENABLED = { TRUE | FALSE }
  [ ALLOWED_RECIPIENTS = ( '<email_address>' [ , ... '<email_address>' ] ) ]
  [ DEFAULT_RECIPIENTS = ( '<email_address>' [ , ... '<email_address>' ] ) ]
  [ DEFAULT_SUBJECT = '<subject_line>' ]
  [ COMMENT = '<string_literal>' ]
```

### TYPE = QUEUE, NOTIFICATION_PROVIDER = AWS_SNS (Outbound)

```sql
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ENABLED = { TRUE | FALSE }
  TYPE = QUEUE
  DIRECTION = OUTBOUND
  NOTIFICATION_PROVIDER = AWS_SNS
  AWS_SNS_TOPIC_ARN = '<topic_arn>'
  AWS_SNS_ROLE_ARN = '<iam_role_arn>'
  [ COMMENT = '<string_literal>' ]
```

### TYPE = QUEUE, NOTIFICATION_PROVIDER = AZURE_EVENT_GRID (Outbound)

```sql
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ENABLED = { TRUE | FALSE }
  TYPE = QUEUE
  DIRECTION = OUTBOUND
  NOTIFICATION_PROVIDER = AZURE_EVENT_GRID
  AZURE_EVENT_GRID_TOPIC_ENDPOINT = '<event_grid_topic_endpoint>'
  AZURE_TENANT_ID = '<ad_directory_id>'
  [ COMMENT = '<string_literal>' ]
```

### TYPE = QUEUE, NOTIFICATION_PROVIDER = GCP_PUBSUB (Outbound)

```sql
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  ENABLED = { TRUE | FALSE }
  TYPE = QUEUE
  DIRECTION = OUTBOUND
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  GCP_PUBSUB_TOPIC_NAME = '<topic_id>'
  [ COMMENT = '<string_literal>' ]
```

### TYPE = WEBHOOK

```sql
CREATE [ OR REPLACE ] NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
  TYPE = WEBHOOK
  ENABLED = { TRUE | FALSE }
  WEBHOOK_URL = '<url>'
  [ WEBHOOK_SECRET = <secret_name> ]
  [ WEBHOOK_BODY_TEMPLATE = '<template_for_http_request_body>' ]
  [ WEBHOOK_HEADERS = ( '<header_1>'='<value_1>' [ , '<header_N>'='<value_N>', ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| ENABLED | TRUE | Controls whether the integration is active |
| TYPE | (required) | EMAIL, QUEUE, or WEBHOOK |
| DIRECTION | (required for QUEUE) | OUTBOUND |
| NOTIFICATION_PROVIDER | (required for QUEUE) | AWS_SNS, AZURE_EVENT_GRID, or GCP_PUBSUB |
| ALLOWED_RECIPIENTS | Any verified account email | EMAIL only; up to 50 addresses |
| DEFAULT_RECIPIENTS | (none) | EMAIL only |
| DEFAULT_SUBJECT | "Snowflake Email Notification" | EMAIL only; max 256 characters |
| AWS_SNS_TOPIC_ARN | (required for AWS_SNS) | ARN of the SNS topic |
| AWS_SNS_ROLE_ARN | (required for AWS_SNS) | ARN of IAM role with publish permissions |
| AZURE_EVENT_GRID_TOPIC_ENDPOINT | (required for AZURE_EVENT_GRID) | Target Event Grid endpoint URL |
| AZURE_TENANT_ID | (required for AZURE_EVENT_GRID) | Azure AD directory identifier |
| GCP_PUBSUB_TOPIC_NAME | (required for GCP_PUBSUB) | Pub/Sub topic identifier |
| WEBHOOK_URL | (required for WEBHOOK) | HTTPS endpoint URL |
| WEBHOOK_SECRET | (none) | Secret object for sensitive credentials |
| WEBHOOK_BODY_TEMPLATE | (none) | JSON or custom HTTP body template |
| WEBHOOK_HEADERS | (none) | HTTP header key-value pairs |
| COMMENT | (none) | Free-text description |

---

## Common Parameters

### name
- Unique identifier for the integration within the account
- Must start with an alphabetic character
- May contain letters, digits, and underscores; use double quotes for special characters or case-sensitive names

### ENABLED = { TRUE | FALSE }
- `TRUE` (default): integration is active and will send/receive notifications
- `FALSE`: integration is suspended; no notifications are processed

### COMMENT = '<string_literal>'
- Free-text description displayed in `SHOW INTEGRATIONS`
- Default: no value

---

## TYPE = EMAIL Parameters

### ALLOWED_RECIPIENTS = ( '<email_address>' [ , ... ] )
- Comma-separated list of email addresses authorized to receive notifications
- Each address must belong to a current Snowflake account user who has verified their email
- Maximum 50 addresses
- Default: any verified account user email is allowed

### DEFAULT_RECIPIENTS = ( '<email_address>' [ , ... ] )
- Default list of recipients when none are specified in the notification call
- Addresses must be a subset of ALLOWED_RECIPIENTS (if set)
- Default: none

### DEFAULT_SUBJECT = '<subject_line>'
- Default email subject line used when the caller does not supply one
- Maximum 256 characters
- Default: `"Snowflake Email Notification"`
- Can be overridden per-call via `EMAIL_INTEGRATION_CONFIG` helper function

---

## TYPE = QUEUE (AWS SNS) Parameters

### AWS_SNS_TOPIC_ARN = '<topic_arn>'
- Amazon Resource Name (ARN) of the SNS topic that will receive notifications
- Format: `arn:aws:sns:<region>:<account-id>:<topic-name>`
- Required for `NOTIFICATION_PROVIDER = AWS_SNS`

### AWS_SNS_ROLE_ARN = '<iam_role_arn>'
- ARN of the IAM role that Snowflake assumes to publish messages to the SNS topic
- Case-sensitive
- The role must have `sns:Publish` permission on the specified topic
- Required for `NOTIFICATION_PROVIDER = AWS_SNS`

**Cloud restriction**: Available only for Snowflake accounts hosted on AWS.

---

## TYPE = QUEUE (Azure Event Grid) Parameters

### AZURE_EVENT_GRID_TOPIC_ENDPOINT = '<event_grid_topic_endpoint>'
- Full HTTPS endpoint URL of the Azure Event Grid topic
- Required for `NOTIFICATION_PROVIDER = AZURE_EVENT_GRID`

### AZURE_TENANT_ID = '<ad_directory_id>'
- Azure Active Directory (AAD) tenant/directory ID
- Required for `NOTIFICATION_PROVIDER = AZURE_EVENT_GRID`

**Cloud restriction**: Available only for Snowflake accounts hosted on Microsoft Azure. Government cloud regions cannot exchange notifications with commercial regions.

---

## TYPE = QUEUE (GCP Pub/Sub) Parameters

### GCP_PUBSUB_TOPIC_NAME = '<topic_id>'
- Google Cloud Pub/Sub topic identifier
- Required for `NOTIFICATION_PROVIDER = GCP_PUBSUB`

**Cloud restriction**: Available only for Snowflake accounts hosted on Google Cloud Platform (GCP).

---

## TYPE = WEBHOOK Parameters

### WEBHOOK_URL = '<url>'
- HTTPS endpoint URL that will receive the webhook POST request
- Required for `TYPE = WEBHOOK`
- Supported targets include Slack (`https://hooks.slack.com/services/...`), Microsoft Teams, and PagerDuty (`https://events.pagerduty.com/v2/enqueue`)
- For Microsoft Teams URLs, omit port 443

### WEBHOOK_SECRET = <secret_name>
- References a Snowflake Secret object that stores sensitive credentials (e.g., API tokens, bearer tokens)
- Qualified name format: `<db>.<schema>.<secret_name>`
- Use the `SNOWFLAKE_WEBHOOK_SECRET` placeholder in `WEBHOOK_BODY_TEMPLATE` or `WEBHOOK_HEADERS` to inject the secret value at send time
- Requires `USAGE` privilege on the referenced secret
- Default: no value

### WEBHOOK_BODY_TEMPLATE = '<template>'
- HTTP request body template in JSON or another format accepted by the target service
- Use `SNOWFLAKE_WEBHOOK_MESSAGE` as a placeholder for the notification message text
- Use `SNOWFLAKE_WEBHOOK_SECRET` as a placeholder for the secret value
- When set, `Content-Type` must also be included in `WEBHOOK_HEADERS`
- Default: no value

### WEBHOOK_HEADERS = ( '<header>'='<value>' [ , ... ] )
- HTTP request headers sent with each webhook call
- Use `SNOWFLAKE_WEBHOOK_SECRET` as a placeholder in header values for sensitive data
- Default: no value

---

## Access Control Requirements
- `CREATE INTEGRATION` privilege on the account (held by ACCOUNTADMIN by default)
- `USAGE` privilege on any referenced Secret object (WEBHOOK_SECRET)
- Appropriate cloud-side permissions (IAM role for AWS, Azure SP, GCP service account)
