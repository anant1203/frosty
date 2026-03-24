---
name: snowflake-create-api-integration
description: Consult Snowflake CREATE API INTEGRATION parameter reference before generating any CREATE API INTEGRATION DDL.
---

Before writing a CREATE API INTEGRATION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE API INTEGRATION IF NOT EXISTS`.
5. This skill focuses on Amazon API Gateway (`API_PROVIDER = aws_api_gateway`); for private endpoints use `aws_private_api_gateway`; for GovCloud use `aws_gov_api_gateway` or `aws_gov_private_api_gateway`.
6. `API_AWS_ROLE_ARN` must reference an IAM role that Snowflake can assume; after creation, the user must update the IAM trust policy with the `API_AWS_IAM_USER_ARN` and `API_AWS_EXTERNAL_ID` values from `DESCRIBE INTEGRATION`.
7. `API_ALLOWED_PREFIXES` is treated as a URL prefix match — ensure it is restrictive enough to cover only the intended endpoints.
