# CREATE DATABASE ROLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-database-role

## Full Syntax

```sql
CREATE [ OR REPLACE ] DATABASE ROLE [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
```

## Variant: CREATE OR ALTER DATABASE ROLE (Preview Feature)

```sql
CREATE OR ALTER DATABASE ROLE <name>
  [ COMMENT = '<string_literal>' ]
```

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Identifier for the database role. Must be unique within the database in which it is created. Must begin with an alphabetic character. Cannot contain spaces or special characters unless enclosed in double quotes (double-quoted identifiers are case-sensitive). If not fully qualified as `<db_name>.<database_role_name>`, the role is created in the current session database. |

## Optional Parameters Defaults Table

| Parameter | Default |
|-----------|---------|
| `COMMENT` | No value (NULL) |

## Optional Parameters — Detailed Descriptions

**`COMMENT = '<string_literal>'`**
A free-text description of the database role's purpose and intended privilege scope. Strongly recommended for governance. Default: no value.

## Behavioral Notes

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive and cannot both appear in the same statement.
- `CREATE OR REPLACE DATABASE ROLE` drops and recreates the role atomically. If the role was included in a share, it is removed from that share.
- Upon creation, Snowflake automatically grants the `USAGE` privilege on the containing database to the new database role. No explicit GRANT for database USAGE is needed.
- Database roles are scoped to a single database and cannot span databases.
- Database roles can be created in catalog-linked (Snowflake Open Catalog) databases.
- For `CREATE OR ALTER DATABASE ROLE`: existing tags remain unchanged; tag modification through this form is unsupported.
- Avoid storing personal, sensitive, or regulated data in the role name or comment (Snowflake metadata restriction).

## Access Control Requirements

| Privilege | Object | Notes |
|-----------|--------|-------|
| CREATE DATABASE ROLE | Database | Required to create a new database role within a specific database. |
| OWNERSHIP | Database role | Required to run CREATE OR ALTER DATABASE ROLE on an existing role. |
