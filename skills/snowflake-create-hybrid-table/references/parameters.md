# CREATE HYBRID TABLE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-hybrid-table

---

## Full Syntax

```sql
CREATE [ OR REPLACE ] HYBRID TABLE [ IF NOT EXISTS ] <table_name>
  (
    <col_name> <col_type>
    [
      {
        DEFAULT <expr>
        | { AUTOINCREMENT | IDENTITY }
          [
            {
              ( <start_num> , <step_num> )
              | START <num> INCREMENT <num>
            }
          ]
          [ { ORDER | NOORDER } ]
      }
    ]
    [ NOT NULL ]
    [ inlineConstraint ]
    [ COLLATE '<collation_specification>' ]
    [ COMMENT '<string_literal>' ]
    [ , <col_name> <col_type> [ ... ] ]
    [ , outoflineConstraint ]
    [ , outoflineIndex ]
    [ , ... ]
  )
  [ COMMENT = '<string_literal>' ]
```

### inlineConstraint syntax

```sql
[ CONSTRAINT <constraint_name> ]
{ UNIQUE
  | PRIMARY KEY
  | [ FOREIGN KEY ] REFERENCES <ref_table> [ ( <ref_col> ) ]
    [ MATCH { FULL | PARTIAL | SIMPLE } ]
    [ ON [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
         [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
}
[ NOT ENFORCED | ENFORCED ]   -- NOTE: NOT ENFORCED is not permitted on hybrid tables
[ DEFERRABLE | NOT DEFERRABLE ]
[ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]
```

### outoflineConstraint syntax

```sql
[ CONSTRAINT <constraint_name> ]
{ UNIQUE ( <col_name> [ , <col_name> , ... ] )
  | PRIMARY KEY ( <col_name> [ , <col_name> , ... ] )
  | [ FOREIGN KEY ] ( <col_name> [ , ... ] )
    REFERENCES <ref_table> [ ( <ref_col> [ , ... ] ) ]
    [ MATCH { FULL | PARTIAL | SIMPLE } ]
    [ ON [ DELETE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ]
         [ UPDATE { CASCADE | SET NULL | SET DEFAULT | RESTRICT | NO ACTION } ] ]
}
```

### outoflineIndex syntax

```sql
INDEX <index_name> ( <col_name> [ , <col_name> , ... ] )
  [ INCLUDE ( <col_name> [ , <col_name> , ... ] ) ]
```

---

## Defaults Table

| Parameter | Default | Notes |
|-----------|---------|-------|
| `PRIMARY KEY` | **Required** — no default | Must define at least one primary key (inline or out-of-line) |
| `DEFAULT <expr>` | No default value | Constant, simple expression, or sequence reference |
| `AUTOINCREMENT` / `IDENTITY` start | `1` | Starting value for auto-increment column |
| `AUTOINCREMENT` / `IDENTITY` step | `1` | Increment step |
| `AUTOINCREMENT` ordering | `ORDER` | Use `NOORDER` for better point-write performance |
| `NOT NULL` | Nulls allowed | Enforced at DML time |
| `COLLATE` | None (account default) | Not supported on PK or indexed columns |
| `COMMENT` (column) | None | Free-text column description |
| `COMMENT` (table) | None | Free-text table description |
| Constraint enforcement | `ENFORCED` | `NOT ENFORCED` is **not** permitted on hybrid tables |

---

## Parameter Descriptions

### table_name *(required)*
Unique identifier for the hybrid table within the schema. Must start with an alphabetic character. Enclose in double quotes if the name contains spaces or special characters.

### col_name *(required)*
Column identifier. Follows the same naming rules as table names.

### col_type *(required)*
SQL data type for the column. Refer to the Snowflake SQL data types reference for supported types.

### PRIMARY KEY *(required)*
At least one primary key constraint is **mandatory** on every hybrid table. It may be:

- **Inline** (single-column): `<col_name> <col_type> PRIMARY KEY`
- **Out-of-line** (single or composite): `PRIMARY KEY (<col1> [, <col2>, ...])`

Primary key columns are stored as Iceberg identifier fields in metadata. The constraint is **enforced** at the row level.

### DEFAULT \<expr\>
Specifies the default value for the column when no value is provided in an INSERT statement. Supported forms:
- Literal constants
- Simple expressions
- References to sequences

### AUTOINCREMENT / IDENTITY
Automatically generates sequential numeric values. Equivalent aliases.

- `( <start_num>, <step_num> )` or `START <num> INCREMENT <num>` — configure start and step.
- `ORDER` (default): values are assigned in strict ascending order.
- `NOORDER`: values may be assigned out of order, enabling higher point-write throughput. Recommended for surrogate keys where ordering is not required.

### NOT NULL
Prevents the column from accepting NULL values. Enforced at the row level by Snowflake.

### CONSTRAINT \<constraint_name\>
Optional name for a constraint. Named constraints can be referenced in ALTER TABLE statements.

### UNIQUE
Enforces column-level uniqueness. Enforced at the row level. Cannot be set as `NOT ENFORCED`.

### FOREIGN KEY … REFERENCES
Enforces referential integrity between columns of two hybrid tables. Foreign key columns **cannot** be NULL. Supported referential actions: `CASCADE`, `SET NULL`, `SET DEFAULT`, `RESTRICT`, `NO ACTION`.

### INDEX \<index_name\>
Creates a secondary index on specified columns to improve point-lookup and range-scan performance.

- `INCLUDE (<col_name> [, ...])`: adds extra columns to the index leaf pages (covering index), improving SELECT queries that reference those columns without requiring a table lookup.

### COLLATE '\<collation_specification\>'
Sets the string comparison collation for text columns. **Not supported** on primary key columns or indexed columns. To disable a database-level `DEFAULT_DDL_COLLATION`, set `COLLATE ''` explicitly.

### COMMENT (column / table)
Free-text documentation string. Can be set at both the column level (inline) and the table level (as `COMMENT = '...'`).

---

## Important Usage Notes

- **Primary key is mandatory.** The CREATE statement fails without at least one PRIMARY KEY constraint.
- `PRIMARY KEY`, `UNIQUE`, and `FOREIGN KEY` constraints are all **enforced** at the row level; `NOT ENFORCED` is not a valid option for hybrid tables.
- Constraints cannot be altered after table creation.
- Foreign key columns cannot be NULL.
- Hybrid tables **cannot** be `TEMPORARY` or `TRANSIENT`.
- Cloning hybrid tables is not supported within transient schemas or databases.
- Available only in **AWS and Microsoft Azure commercial regions** — not available in GCP or government regions.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
