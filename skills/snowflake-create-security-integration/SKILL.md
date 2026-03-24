---
name: snowflake-create-security-integration
description: Consult Snowflake CREATE SECURITY INTEGRATION parameter reference before generating any CREATE SECURITY INTEGRATION DDL.
---

Before writing a CREATE SECURITY INTEGRATION statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE SECURITY INTEGRATION IF NOT EXISTS`.
5. Select the correct TYPE based on the use case:
   - `API_AUTHENTICATION` — for connecting Snowflake to external APIs via OAuth2 (used with EXTERNAL ACCESS INTEGRATION and SECRETs).
   - `AWS_IAM` — for authenticating Snowflake with AWS services using IAM roles.
   - `EXTERNAL_OAUTH` — for allowing external OAuth providers (Okta, Azure AD, custom) to authorize Snowflake access.
   - `OAUTH` — for Snowflake-managed OAuth flows (Snowflake OAuth for partners or custom clients).
   - `SAML2` — for SAML-based SSO from an identity provider.
   - `SCIM` — for provisioning and managing users and groups via SCIM 2.0.
6. Each TYPE has mutually exclusive required parameters; only include parameters documented for the selected TYPE.
7. For SAML2, the SAML2_X509_CERT value must be the raw base64-encoded certificate without PEM headers.
