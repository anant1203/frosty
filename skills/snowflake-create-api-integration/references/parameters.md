# CREATE API INTEGRATION — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-api-integration

## Syntax — Amazon API Gateway (Primary Focus)

```sql
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = { aws_api_gateway | aws_private_api_gateway | aws_gov_api_gateway | aws_gov_private_api_gateway }
  API_AWS_ROLE_ARN = '<iam_role>'
  [ API_KEY = '<api_key>' ]
  API_ALLOWED_PREFIXES = ('<url_prefix>' [, '<url_prefix>' ...])
  [ API_BLOCKED_PREFIXES = ('<url_prefix>' [, '<url_prefix>' ...]) ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

## Syntax — Azure API Management

```sql
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = azure_api_management
  AZURE_TENANT_ID = '<tenant_id>'
  AZURE_AD_APPLICATION_ID = '<app_id>'
  [ API_KEY = '<api_key>' ]
  API_ALLOWED_PREFIXES = ('<url_prefix>' [, '<url_prefix>' ...])
  [ API_BLOCKED_PREFIXES = ('<url_prefix>' [, '<url_prefix>' ...]) ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

## Syntax — Google Cloud API Gateway

```sql
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = google_api_gateway
  GOOGLE_AUDIENCE = '<google_audience>'
  API_ALLOWED_PREFIXES = ('<url_prefix>' [, '<url_prefix>' ...])
  [ API_BLOCKED_PREFIXES = ('<url_prefix>' [, '<url_prefix>' ...]) ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| API_PROVIDER | — (required) |
| API_AWS_ROLE_ARN | — (required for AWS) |
| AZURE_TENANT_ID | — (required for Azure) |
| AZURE_AD_APPLICATION_ID | — (required for Azure) |
| GOOGLE_AUDIENCE | — (required for GCP) |
| API_KEY | — (not set) |
| API_ALLOWED_PREFIXES | — (required) |
| API_BLOCKED_PREFIXES | — (not set) |
| ENABLED | `TRUE` |
| COMMENT | — |

## Parameter Descriptions

### `<integration_name>` (required)
Unique identifier for the API integration. Must follow standard Snowflake object identifier rules (start with alphabetic character, enclose special characters in double quotes).

### `API_PROVIDER` (required)
Specifies the cloud platform HTTPS proxy service type.

| Value | Description |
|-------|-------------|
| `aws_api_gateway` | Amazon API Gateway (public) |
| `aws_private_api_gateway` | Amazon API Gateway via AWS PrivateLink |
| `aws_gov_api_gateway` | Amazon API Gateway in AWS GovCloud (public) |
| `aws_gov_private_api_gateway` | Amazon API Gateway in AWS GovCloud via PrivateLink |
| `azure_api_management` | Azure API Management service |
| `google_api_gateway` | Google Cloud API Gateway |
| `git_https_api` | Git repository HTTPS endpoints |

### `API_AWS_ROLE_ARN` (required for AWS providers)
The Amazon Resource Name (ARN) of the IAM role that Snowflake will assume to call the API. Format: `arn:aws:iam::<account_id>:role/<role_name>`.

After creation, retrieve `API_AWS_IAM_USER_ARN` and `API_AWS_EXTERNAL_ID` from `DESCRIBE INTEGRATION <name>` and add them to the IAM role's trust policy.

### `API_KEY`
An API key (subscription key) for the service, if the API Gateway endpoint requires one. Stored securely. Default: not set.

### `API_ALLOWED_PREFIXES` (required)
A comma-separated list of HTTPS URL prefixes that define which external function endpoints this integration can reach. Snowflake treats each value as a prefix match — the endpoint URL of an external function must start with one of these prefixes.

Example: `('https://xyz.execute-api.us-east-1.amazonaws.com/prod/')`

### `API_BLOCKED_PREFIXES`
A comma-separated list of HTTPS URL prefixes explicitly blocked, even if they match an allowed prefix. Useful for excluding specific sub-paths from a broad allowed prefix. Default: not set.

### `ENABLED` (required)
Whether the integration is active.

- `TRUE` — integration is active (default)
- `FALSE` — integration is disabled

### `AZURE_TENANT_ID` (required for Azure)
The tenant ID (Directory ID) of the Azure Active Directory tenant that manages the Azure AD application.

### `AZURE_AD_APPLICATION_ID` (required for Azure)
The application (client) ID of the Azure AD application registered for the integration.

### `GOOGLE_AUDIENCE` (required for GCP)
The audience value for the Google Cloud API Gateway, used for JWT authentication.

### `COMMENT`
A descriptive string for the integration. Default: none.
