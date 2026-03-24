# CREATE PACKAGES POLICY — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-packages-policy

## Syntax

```sql
CREATE [ OR REPLACE ] PACKAGES POLICY [ IF NOT EXISTS ] <name>
  LANGUAGE PYTHON
  [ ALLOWLIST = ( [ '<packageSpec>' ] [ , '<packageSpec>' ... ] ) ]
  [ BLOCKLIST = ( [ '<packageSpec>' ] [ , '<packageSpec>' ... ] ) ]
  [ ADDITIONAL_CREATION_BLOCKLIST = ( [ '<packageSpec>' ] [ , '<packageSpec>' ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| LANGUAGE | — (required, only `PYTHON` supported) |
| ALLOWLIST | `('*')` — all packages allowed |
| BLOCKLIST | `()` — no packages blocked |
| ADDITIONAL_CREATION_BLOCKLIST | `()` — no additional creation blocks |
| COMMENT | — |

## Parameter Descriptions

### `<name>` (required)
A unique identifier for the packages policy within the schema. Must start with an alphabetic character; enclose in double quotes if the name contains special characters.

### `LANGUAGE PYTHON` (required)
Specifies the programming language this policy applies to. Currently only `PYTHON` is supported.

### `ALLOWLIST`
A list of package specifications that are permitted for use in Python UDFs and stored procedures.

Package spec formats:
- `'*'` — wildcard, allows all packages (default)
- `'package_name'` — allows any version of the package
- `'package_name==1.2.3'` — allows only the specified version
- `'package_name>=1.0'` — allows versions satisfying the constraint

When specifying an explicit allow list, only packages matching the listed specs will be permitted. Setting to `()` blocks all packages.

### `BLOCKLIST`
A list of package specifications that are blocked at runtime. Takes precedence over ALLOWLIST entries. To unset an existing blocklist, specify an empty list `()`.

Package spec format same as ALLOWLIST.

### `ADDITIONAL_CREATION_BLOCKLIST`
A list of package specifications that are blocked both at creation time and at runtime. Applies to temporary UDFs and anonymous procedures. Useful for packages that should never appear in any code, even transiently.

Package spec format same as ALLOWLIST.

### `COMMENT`
A descriptive string for the packages policy. Default: none.

## Access Control Prerequisites

- Requires `CREATE PACKAGES POLICY` privilege on the schema.
- The policy must be attached at the account level via `ALTER ACCOUNT SET PACKAGES POLICY` to take effect.
