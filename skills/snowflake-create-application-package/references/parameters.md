# CREATE APPLICATION PACKAGE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-application-package

---

## Overview

`CREATE APPLICATION PACKAGE` is the foundational DDL for the **Snowflake Native App Framework**. A provider creates an application package as the container that holds all versions, release directives, and setup scripts for a Snowflake Native App. The package is listed on the Snowflake Marketplace (EXTERNAL) or shared within an organization (INTERNAL).

Requires the `CREATE APPLICATION PACKAGE` privilege at the account level (granted to ACCOUNTADMIN by default).

---

## Full Syntax

```sql
CREATE APPLICATION PACKAGE [ IF NOT EXISTS ] <name>
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ DISTRIBUTION = { INTERNAL | EXTERNAL } ]
  [ LISTING_AUTO_REFRESH = { TRUE | FALSE } ]
  [ MULTIPLE_INSTANCES = TRUE ]
  [ ENABLE_RELEASE_CHANNELS = TRUE | FALSE ]
```

> Note: `CREATE OR REPLACE` is **not** supported. Use `IF NOT EXISTS` to avoid duplicate-creation errors.

---

## Defaults Table

| Parameter | Default Value |
|-----------|---------------|
| `DATA_RETENTION_TIME_IN_DAYS` | `1` |
| `MAX_DATA_EXTENSION_TIME_IN_DAYS` | — (account/object default) |
| `DEFAULT_DDL_COLLATION` | — (none; inherits account default) |
| `COMMENT` | — (none) |
| `TAG` | — (none) |
| `DISTRIBUTION` | — (not set; effectively `INTERNAL` until explicitly set) |
| `LISTING_AUTO_REFRESH` | — (not set) |
| `MULTIPLE_INSTANCES` | — (not set; consumers limited to one instance) |
| `ENABLE_RELEASE_CHANNELS` | — (not set; defaults to FALSE behavior) |

---

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the application package within the Snowflake account. Must start with an alphabetic character. Names containing special characters or spaces must be enclosed in double quotes (e.g. `"My App Package"`).

---

### `DATA_RETENTION_TIME_IN_DAYS = <integer>`
The number of days for which Snowflake retains historical data to support Time Travel operations (`CLONE`, `UNDROP`, `AT | BEFORE` queries) on the application package.

**Valid values:**
- Standard Edition accounts: `0` or `1`
- Enterprise Edition (and above): `0` to `90`

**Default:** `1`

Setting to `0` disables Time Travel for this object.

---

### `MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer>`
The maximum number of additional days Snowflake can extend the data retention period to prevent streams on the package from becoming stale. When a stream's offset approaches the retention period boundary, Snowflake may automatically extend retention up to this cap.

**Valid values:** Integer (bounded by account edition limits; cannot exceed `DATA_RETENTION_TIME_IN_DAYS` maximum for the edition).
**Default:** Account or object-level default.

---

### `DEFAULT_DDL_COLLATION = '<collation_specification>'`
Sets the default collation specification applied to all new tables and schemas created within the application package unless overridden at a lower level.

**Valid values:** Any valid Snowflake collation specification string (e.g. `'en-ci'`, `'utf8'`).
**Default:** None (inherits account-level default collation).

---

### `COMMENT = '<string_literal>'`
A free-text description for the application package. Visible in `SHOW APPLICATION PACKAGES`, the Snowsight UI, and on Snowflake Marketplace listings.

**Valid values:** String literal, maximum 256 characters.
**Default:** None.

---

### `TAG ( <tag_name> = '<tag_value>' [ , ... ] )`
Associates one or more object tags with the application package for governance, cost attribution, and data classification purposes. The `WITH` keyword is optional.

**Valid values:** One or more `tag_name = 'tag_value'` pairs where each tag must already exist in the account.
**Default:** None.

---

### `DISTRIBUTION = { INTERNAL | EXTERNAL }`
Controls the scope of the Snowflake Marketplace listing generated from this application package.

| Value | Description |
|-------|-------------|
| `INTERNAL` | The application can only be shared within the provider's organization. No external listing is created. |
| `EXTERNAL` | The application can be listed on the Snowflake Marketplace and shared with any Snowflake account. Triggers an automated Snowflake security review before the listing goes live. |

**Default:** Not set (the package is created without a distribution scope; behaves as `INTERNAL` until explicitly set).

**Important:** Switching to `EXTERNAL` initiates a security scan by Snowflake; ensure the setup script and referenced objects comply with Snowflake's security policies before setting this value.

---

### `LISTING_AUTO_REFRESH = { TRUE | FALSE }`
When `TRUE`, Snowflake automatically replicates the application package to consumer accounts whenever a new release directive is created or updated, without requiring manual refresh operations.

**Valid values:** `TRUE` or `FALSE`.
**Default:** Not set.

---

### `MULTIPLE_INSTANCES = TRUE`
Allows consumers to install more than one instance of the application in their account. When enabled, consumers may install up to **10 instances** per account.

**Valid values:** `TRUE` only (once set to `TRUE` it cannot be reverted to `FALSE`).
**Default:** Not set (consumers limited to a single installation).

**Warning:** This setting is **irreversible**. Confirm with the user before including it.

---

### `ENABLE_RELEASE_CHANNELS = { TRUE | FALSE }`
Enables the release channels feature for the application package, allowing providers to define named channels (e.g. `STABLE`, `BETA`) and assign consumers to specific channels for controlled rollout of new versions.

**Valid values:** `TRUE` or `FALSE`. Once set to `TRUE`, it **cannot be reverted**.
**Default:** Not set (equivalent to `FALSE`).

**Warning:** Setting to `TRUE` is **irreversible**. Confirm with the user before including it.
