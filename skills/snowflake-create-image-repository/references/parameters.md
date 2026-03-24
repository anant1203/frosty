# Snowflake CREATE IMAGE REPOSITORY — Parameter Reference

## Syntax

```sql
CREATE [ OR REPLACE ] IMAGE REPOSITORY [ IF NOT EXISTS ] <name>
  [ ENCRYPTION = ( TYPE = 'SNOWFLAKE_FULL' | TYPE = 'SNOWFLAKE_SSE' ) ]
```

---

## Parameter Defaults

| Parameter | Default | Notes |
|---|---|---|
| ENCRYPTION TYPE | SNOWFLAKE_FULL | Cannot be changed after creation |

---

## Required Parameters

### name
- Unique identifier for the image repository within the schema
- Must start with an alphabetic character
- Quoted names (for special characters or case-sensitivity) are **not** supported
- The same no-quote constraint applies to the containing database and schema names

---

## Optional Parameters

### ENCRYPTION = ( TYPE = 'SNOWFLAKE_FULL' | TYPE = 'SNOWFLAKE_SSE' )

Controls the encryption mode for container image binaries stored in the repository. This setting **cannot be changed after the repository is created**.

#### TYPE = 'SNOWFLAKE_FULL' (Default)
- Applies both on-host (image registry host) encryption **and** server-side encryption
- On-host encryption: AES-GCM with a 128-bit key by default; can be upgraded to 256-bit via the `CLIENT_ENCRYPTION_KEY_SIZE` account parameter
- Server-side encryption: AES-256 strong encryption applied automatically by the cloud provider
- Supports **Tri-Secret Secure** (customer-managed keys via key management integration)
- Use this type when Tri-Secret Secure compliance or maximum encryption depth is required

#### TYPE = 'SNOWFLAKE_SSE'
- Applies server-side encryption only (cloud-provider managed, e.g., Amazon S3 SSE)
- Does **not** apply on-host encryption
- Does **not** support Tri-Secret Secure
- Use this type when on-host encryption overhead is undesirable and Tri-Secret Secure is not required

---

## Access Control Requirements
- `CREATE IMAGE REPOSITORY` privilege on the schema
- The repository is scoped to the current database and schema at creation time
