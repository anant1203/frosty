# CREATE SECURITY INTEGRATION — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-security-integration

## Overview

The syntax for CREATE SECURITY INTEGRATION varies significantly by TYPE. Select the section matching the desired integration type.

---

## TYPE = API_AUTHENTICATION (OAuth2 — Client Credentials Flow)

```sql
CREATE SECURITY INTEGRATION <name>
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = OAUTH2
  ENABLED = { TRUE | FALSE }
  [ OAUTH_TOKEN_ENDPOINT = '<string_literal>' ]
  [ OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST } ]
  [ OAUTH_CLIENT_ID = '<string_literal>' ]
  [ OAUTH_CLIENT_SECRET = '<string_literal>' ]
  [ OAUTH_GRANT = 'CLIENT_CREDENTIALS' ]
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_ALLOWED_SCOPES = ( '<scope_1>' [ , '<scope_2>' ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

## TYPE = API_AUTHENTICATION (OAuth2 — Authorization Code Grant Flow)

```sql
CREATE SECURITY INTEGRATION <name>
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = OAUTH2
  ENABLED = { TRUE | FALSE }
  [ OAUTH_AUTHORIZATION_ENDPOINT = '<string_literal>' ]
  [ OAUTH_TOKEN_ENDPOINT = '<string_literal>' ]
  [ OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST } ]
  [ OAUTH_CLIENT_ID = '<string_literal>' ]
  [ OAUTH_CLIENT_SECRET = '<string_literal>' ]
  [ OAUTH_GRANT = 'AUTHORIZATION_CODE' ]
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

## TYPE = API_AUTHENTICATION (OAuth2 — JWT Bearer Flow)

```sql
CREATE SECURITY INTEGRATION <name>
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = OAUTH2
  ENABLED = { TRUE | FALSE }
  [ OAUTH_AUTHORIZATION_ENDPOINT = '<string_literal>' ]
  [ OAUTH_TOKEN_ENDPOINT = '<string_literal>' ]
  [ OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST } ]
  [ OAUTH_CLIENT_ID = '<string_literal>' ]
  [ OAUTH_CLIENT_SECRET = '<string_literal>' ]
  [ OAUTH_GRANT = 'JWT_BEARER' ]
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

## TYPE = API_AUTHENTICATION (AWS IAM)

```sql
CREATE SECURITY INTEGRATION <name>
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = AWS_IAM
  AWS_ROLE_ARN = '<iam_role_arn>'
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

### API_AUTHENTICATION Defaults Table

| Parameter | Default |
|-----------|---------|
| ENABLED | `TRUE` |
| OAUTH_CLIENT_AUTH_METHOD | `CLIENT_SECRET_BASIC` |
| OAUTH_ALLOWED_SCOPES | `[]` (empty — all scopes permitted) |
| OAUTH_GRANT | — (not set) |
| OAUTH_ACCESS_TOKEN_VALIDITY | — (not set; use server default) |
| OAUTH_REFRESH_TOKEN_VALIDITY | — (not set) |
| COMMENT | — |

### API_AUTHENTICATION Parameter Descriptions

**`TYPE = API_AUTHENTICATION`** — Creates a security interface between Snowflake and an external service using OAuth 2.0 or AWS IAM credentials.

**`AUTH_TYPE`** (required) — The authentication mechanism.
- `OAUTH2` — Use OAuth 2.0 flows
- `AWS_IAM` — Use AWS IAM role credentials

**`ENABLED`** — Whether the integration is active. Default: `TRUE`.

**`OAUTH_AUTHORIZATION_ENDPOINT`** — URL of the OAuth authorization server's authorization endpoint. Used in authorization-code and JWT-bearer flows.

**`OAUTH_TOKEN_ENDPOINT`** — URL of the OAuth authorization server's token endpoint for obtaining access tokens.

**`OAUTH_CLIENT_AUTH_METHOD`** — How client credentials are sent to the token endpoint.
- `CLIENT_SECRET_BASIC` — Credentials in HTTP Basic Authorization header (default)
- `CLIENT_SECRET_POST` — Credentials in HTTP POST body

**`OAUTH_CLIENT_ID`** — The client identifier assigned by the OAuth authorization server.

**`OAUTH_CLIENT_SECRET`** — The client secret assigned by the OAuth authorization server. Stored encrypted.

**`OAUTH_GRANT`** — The OAuth flow type.
- `'CLIENT_CREDENTIALS'` — Machine-to-machine flow with no user involvement
- `'AUTHORIZATION_CODE'` — Three-legged OAuth with user authorization
- `'JWT_BEARER'` — JWT assertion flow

**`OAUTH_ACCESS_TOKEN_VALIDITY`** — Default lifetime of OAuth access tokens, in seconds. If not set, uses the authorization server's default.

**`OAUTH_REFRESH_TOKEN_VALIDITY`** — Refresh token validity, in seconds.

**`OAUTH_ALLOWED_SCOPES`** — Scopes that may be requested when using client-credentials flow. Default: empty list (all scopes allowed).

**`AWS_ROLE_ARN`** (required for AWS_IAM) — ARN of the AWS IAM role that Snowflake will assume. Format: `arn:aws:iam::<account_id>:role/<role_name>`.

---

## TYPE = EXTERNAL_OAUTH

```sql
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
  <name>
  TYPE = EXTERNAL_OAUTH
  ENABLED = { TRUE | FALSE }
  EXTERNAL_OAUTH_TYPE = { OKTA | AZURE | PING_FEDERATE | CUSTOM }
  EXTERNAL_OAUTH_ISSUER = '<string_literal>'
  EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = { '<string_literal>' | ('<string_literal>' [ , '<string_literal>' , ... ] ) }
  EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = { 'LOGIN_NAME' | 'EMAIL_ADDRESS' }
  [ EXTERNAL_OAUTH_JWS_KEYS_URL = { '<string_literal>' | ('<string_literal>' [ , '<string_literal>' , ... ] ) } ]
  [ EXTERNAL_OAUTH_BLOCKED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ EXTERNAL_OAUTH_ALLOWED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ EXTERNAL_OAUTH_RSA_PUBLIC_KEY = <public_key1> ]
  [ EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 = <public_key2> ]
  [ EXTERNAL_OAUTH_AUDIENCE_LIST = { '<string_literal>' | ('<string_literal>' [ , '<string_literal>' , ... ] ) } ]
  [ EXTERNAL_OAUTH_ANY_ROLE_MODE = { DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE } ]
  [ EXTERNAL_OAUTH_SCOPE_DELIMITER = '<string_literal>' ]
  [ EXTERNAL_OAUTH_SCOPE_MAPPING_ATTRIBUTE = '<string_literal>' ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ COMMENT = '<string_literal>' ]
```

### EXTERNAL_OAUTH Defaults Table

| Parameter | Default |
|-----------|---------|
| ENABLED | `TRUE` |
| EXTERNAL_OAUTH_BLOCKED_ROLES_LIST | ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, SECURITYADMIN |
| EXTERNAL_OAUTH_ANY_ROLE_MODE | `DISABLE` |
| EXTERNAL_OAUTH_SCOPE_DELIMITER | `','` |
| EXTERNAL_OAUTH_JWS_KEYS_URL | — (not set) |
| EXTERNAL_OAUTH_RSA_PUBLIC_KEY | — (not set) |
| EXTERNAL_OAUTH_AUDIENCE_LIST | Account URL only |
| NETWORK_POLICY | — (not set) |
| COMMENT | — |

### EXTERNAL_OAUTH Parameter Descriptions

**`EXTERNAL_OAUTH_TYPE`** (required) — The external OAuth 2.0 authorization server.
- `OKTA` — Okta
- `AZURE` — Microsoft Azure AD / Entra ID
- `PING_FEDERATE` — PingFederate
- `CUSTOM` — any other OIDC-compliant authorization server

**`EXTERNAL_OAUTH_ISSUER`** (required) — HTTPS URL identifying the authorization server. Must match the `iss` claim in tokens.

**`EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM`** (required) — The JWT claim(s) used to identify the Snowflake user. Single string or list.

**`EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`** (required) — The Snowflake user attribute to match against the mapping claim.
- `'LOGIN_NAME'` — match against the user's login name
- `'EMAIL_ADDRESS'` — match against the user's email address

**`EXTERNAL_OAUTH_JWS_KEYS_URL`** — HTTPS URL(s) for downloading public keys to validate token signatures. Mutually exclusive with RSA_PUBLIC_KEY parameters.

**`EXTERNAL_OAUTH_RSA_PUBLIC_KEY`** / **`EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2`** — Base64-encoded RSA or ECDSA public keys for token validation. Mutually exclusive with JWS_KEYS_URL.

**`EXTERNAL_OAUTH_BLOCKED_ROLES_LIST`** — Roles that OAuth clients cannot activate. Default includes all admin roles.

**`EXTERNAL_OAUTH_ALLOWED_ROLES_LIST`** — Explicit list of roles OAuth clients may activate. Cannot be used simultaneously with BLOCKED_ROLES_LIST.

**`EXTERNAL_OAUTH_AUDIENCE_LIST`** — Additional accepted `aud` claim values. Default: only the account URL.

**`EXTERNAL_OAUTH_ANY_ROLE_MODE`** — Whether users can request roles not included in the token's scope.
- `DISABLE` — only roles in the token scope allowed (default)
- `ENABLE` — any role allowed
- `ENABLE_FOR_PRIVILEGE` — allowed if user has ENABLE_ANY_ROLE privilege

**`EXTERNAL_OAUTH_SCOPE_DELIMITER`** — Delimiter for scope values in the token. Default: `','`. Custom OAuth type only.

**`EXTERNAL_OAUTH_SCOPE_MAPPING_ATTRIBUTE`** — Token claim containing scope-to-role mappings. Values: `'scp'` or `'scope'`. Custom OAuth type only.

**`NETWORK_POLICY`** — A network policy to restrict client IP addresses for this integration.

---

## TYPE = OAUTH (Snowflake OAuth — Partner Applications)

```sql
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
  <name>
  TYPE = OAUTH
  OAUTH_CLIENT = { TABLEAU_DESKTOP | TABLEAU_SERVER | LOOKER }
  [ OAUTH_REDIRECT_URI = '<uri>' ]  -- Required for LOOKER
  [ ENABLED = { TRUE | FALSE } ]
  [ OAUTH_ISSUE_REFRESH_TOKENS = { TRUE | FALSE } ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED = { TRUE | FALSE } ]
  [ OAUTH_USE_SECONDARY_ROLES = { IMPLICIT | NONE } ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ BLOCKED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
```

## TYPE = OAUTH (Snowflake OAuth — Custom Clients)

```sql
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
  <name>
  TYPE = OAUTH
  OAUTH_CLIENT = CUSTOM
  OAUTH_CLIENT_TYPE = { 'CONFIDENTIAL' | 'PUBLIC' }
  OAUTH_REDIRECT_URI = '<uri>'
  [ ENABLED = { TRUE | FALSE } ]
  [ OAUTH_ALLOW_NON_TLS_REDIRECT_URI = { TRUE | FALSE } ]
  [ OAUTH_ENFORCE_PKCE = { TRUE | FALSE } ]
  [ OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED = { TRUE | FALSE } ]
  [ OAUTH_USE_SECONDARY_ROLES = { IMPLICIT | NONE } ]
  [ PRE_AUTHORIZED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ BLOCKED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ OAUTH_ISSUE_REFRESH_TOKENS = { TRUE | FALSE } ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ OAUTH_CLIENT_RSA_PUBLIC_KEY = <public_key1> ]
  [ OAUTH_CLIENT_RSA_PUBLIC_KEY_2 = <public_key2> ]
  [ USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
```

### OAUTH Defaults Table

| Parameter | Default |
|-----------|---------|
| ENABLED | `TRUE` |
| OAUTH_ISSUE_REFRESH_TOKENS | `TRUE` |
| OAUTH_REFRESH_TOKEN_VALIDITY | `7776000` (90 days, in seconds) |
| OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED | `FALSE` |
| OAUTH_USE_SECONDARY_ROLES | `NONE` |
| OAUTH_ALLOW_NON_TLS_REDIRECT_URI | `FALSE` |
| OAUTH_ENFORCE_PKCE | `FALSE` |
| BLOCKED_ROLES_LIST | ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, SECURITYADMIN |
| USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT | `FALSE` |
| NETWORK_POLICY | — (not set) |
| COMMENT | — |

### OAUTH Parameter Descriptions

**`OAUTH_CLIENT`** (required) — Identifies the client type.
- `TABLEAU_DESKTOP`, `TABLEAU_SERVER`, `LOOKER` — pre-configured partner integrations
- `CUSTOM` — custom OAuth client application

**`OAUTH_CLIENT_TYPE`** (required for CUSTOM) — Whether the client can keep a secret.
- `'CONFIDENTIAL'` — server-side application that can store a secret
- `'PUBLIC'` — client-side/mobile app that cannot keep a secret

**`OAUTH_REDIRECT_URI`** — Redirect URI after successful authorization. Required for LOOKER and CUSTOM clients.

**`OAUTH_ISSUE_REFRESH_TOKENS`** — Whether to issue refresh tokens. Default: `TRUE`.

**`OAUTH_REFRESH_TOKEN_VALIDITY`** — Refresh token lifetime in seconds. Range: 3600–7776000. Default: `7776000` (90 days).

**`OAUTH_ENFORCE_PKCE`** — Require PKCE (Proof Key for Code Exchange) for public clients. Default: `FALSE`.

**`OAUTH_USE_SECONDARY_ROLES`** — Whether to activate secondary roles from the user's default.
- `IMPLICIT` — activate default secondary roles automatically
- `NONE` — no secondary roles (default)

**`BLOCKED_ROLES_LIST`** — Roles that users cannot consent to use via OAuth.

**`PRE_AUTHORIZED_ROLES_LIST`** — Roles that do not require user consent (confidential clients only).

---

## TYPE = SAML2

```sql
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
    <name>
    TYPE = SAML2
    ENABLED = { TRUE | FALSE }
    { METADATA_URL = '<string_literal>' | <idp_parameters> }
    [ ALLOWED_USER_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ ALLOWED_EMAIL_PATTERNS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ SAML2_SP_INITIATED_LOGIN_PAGE_LABEL = '<string_literal>' ]
    [ SAML2_ENABLE_SP_INITIATED = { TRUE | FALSE } ]
    [ SAML2_SNOWFLAKE_X509_CERT = '<string_literal>' ]
    [ SAML2_SIGN_REQUEST = { TRUE | FALSE } ]
    [ SAML2_REQUESTED_NAMEID_FORMAT = '<string_literal>' ]
    [ SAML2_POST_LOGOUT_REDIRECT_URL = '<string_literal>' ]
    [ SAML2_FORCE_AUTHN = { TRUE | FALSE } ]
    [ SAML2_SNOWFLAKE_ISSUER_URL = '<string_literal>' ]
    [ SAML2_SNOWFLAKE_ACS_URL = '<string_literal>' ]
    [ COMMENT = '<string_literal>' ]
```

### IdP Parameters (alternative to METADATA_URL)

```
SAML2_ISSUER = '<string_literal>'
SAML2_SSO_URL = '<string_literal>'
SAML2_PROVIDER = { 'OKTA' | 'ADFS' | 'Custom' }
SAML2_X509_CERT = '<string_literal>'
```

### SAML2 Defaults Table

| Parameter | Default |
|-----------|---------|
| ENABLED | `TRUE` |
| SAML2_ENABLE_SP_INITIATED | — (not set) |
| SAML2_SIGN_REQUEST | — (not set) |
| SAML2_REQUESTED_NAMEID_FORMAT | `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` |
| SAML2_FORCE_AUTHN | `FALSE` |
| SAML2_SNOWFLAKE_ISSUER_URL | Legacy account locator URL |
| SAML2_SNOWFLAKE_ACS_URL | `https://<account>.<region>.snowflakecomputing.com/fed/login` |
| ALLOWED_USER_DOMAINS | — (none) |
| ALLOWED_EMAIL_PATTERNS | — (none) |
| COMMENT | — |

### SAML2 Parameter Descriptions

**`METADATA_URL`** — HTTPS URL of the IdP metadata XML document. Preferred for Okta and Microsoft Entra ID as it allows automatic certificate rotation.

**`SAML2_ISSUER`** — EntityID of the identity provider (alternative to METADATA_URL).

**`SAML2_SSO_URL`** — IdP Single Sign-On URL where Snowflake sends SAML authentication requests.

**`SAML2_PROVIDER`** — The IdP type: `'OKTA'`, `'ADFS'`, or `'Custom'`.

**`SAML2_X509_CERT`** — Base64-encoded X.509 certificate from the IdP (without `-----BEGIN CERTIFICATE-----` / `-----END CERTIFICATE-----` headers).

**`ALLOWED_USER_DOMAINS`** — Email domain allowlist. Only users with matching email domains can authenticate.

**`ALLOWED_EMAIL_PATTERNS`** — Regular expression patterns for email validation.

**`SAML2_SP_INITIATED_LOGIN_PAGE_LABEL`** — The label shown on the SSO button on the Snowflake login page.

**`SAML2_ENABLE_SP_INITIATED`** — Show the SP-initiated SSO button on the login page.

**`SAML2_SNOWFLAKE_X509_CERT`** — Snowflake's signing certificate for signed SAML requests.

**`SAML2_SIGN_REQUEST`** — Whether Snowflake signs outgoing SAML authentication requests.

**`SAML2_FORCE_AUTHN`** — Force the IdP to re-authenticate the user even if a session already exists. Default: `FALSE`.

**`SAML2_SNOWFLAKE_ISSUER_URL`** — The EntityID/Issuer URL Snowflake presents to the IdP. Use the new account identifier URL format for best compatibility.

**`SAML2_SNOWFLAKE_ACS_URL`** — The Assertion Consumer Service URL where the IdP posts SAML responses.

---

## TYPE = SCIM

```sql
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
    <name>
    TYPE = SCIM
    ENABLED = { TRUE | FALSE }
    SCIM_CLIENT = { 'OKTA' | 'AZURE' | 'GENERIC' }
    RUN_AS_ROLE = { 'OKTA_PROVISIONER' | 'AAD_PROVISIONER' | 'GENERIC_SCIM_PROVISIONER' | '<custom_role>' }
    [ NETWORK_POLICY = '<network_policy>' ]
    [ SYNC_PASSWORD = { TRUE | FALSE } ]
    [ COMMENT = '<string_literal>' ]
```

### SCIM Defaults Table

| Parameter | Default |
|-----------|---------|
| ENABLED | `TRUE` |
| SYNC_PASSWORD | `FALSE` |
| NETWORK_POLICY | — (not set) |
| COMMENT | — |

### SCIM Parameter Descriptions

**`SCIM_CLIENT`** (required) — The SCIM 2.0 identity provider client.
- `'OKTA'` — Okta SCIM provisioning
- `'AZURE'` — Microsoft Entra ID (Azure AD) SCIM provisioning
- `'GENERIC'` — Any other SCIM 2.0-compliant provider

**`RUN_AS_ROLE`** (required) — The Snowflake role used to execute SCIM provisioning operations. Must own the users and roles being managed.
- `'OKTA_PROVISIONER'` — built-in role for Okta
- `'AAD_PROVISIONER'` — built-in role for Azure AD
- `'GENERIC_SCIM_PROVISIONER'` — built-in role for generic SCIM
- Custom role name (case-sensitive)

**`SYNC_PASSWORD`** — Whether to sync user passwords from Okta SCIM. Only relevant for SCIM_CLIENT = OKTA. Default: `FALSE`.

**`NETWORK_POLICY`** — A network policy restricting the IP addresses from which SCIM requests are accepted.
