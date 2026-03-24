# CREATE SEQUENCE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-sequence

## Full Syntax

```sql
CREATE [ OR REPLACE ] SEQUENCE [ IF NOT EXISTS ] <name>
  [ WITH ]
  [ START [ WITH ] [ = ] <initial_value> ]
  [ INCREMENT [ BY ] [ = ] <sequence_interval> ]
  [ { ORDER | NOORDER } ]
  [ COMMENT = '<string_literal>' ]
```

## Defaults Table

| Parameter | Default |
|-----------|---------|
| `START` | `1` |
| `INCREMENT` | `1` |
| `ORDER / NOORDER` | Determined by the `NOORDER_SEQUENCE_AS_DEFAULT` account parameter (typically `NOORDER`) |
| `COMMENT` | (none) |

## Parameter Descriptions

### `<name>` *(required)*
Unique identifier for the sequence within its schema. Must start with an alphabetic character. Use double quotes for identifiers containing spaces or special characters (case-sensitive when quoted).

### `START [ WITH ] [ = ] <initial_value>`
The first value the sequence returns. Accepts any 64-bit signed integer (−2⁶³ to 2⁶³ − 1).
Default: `1`.

**Important:** The `START` value is fixed at creation time and cannot be changed via `ALTER SEQUENCE`. If the wrong starting value is set, the sequence must be dropped and recreated.

### `INCREMENT [ BY ] [ = ] <sequence_interval>`
The step added to the current value to produce the next value.
- Positive integer: ascending sequence.
- Negative integer: descending sequence.
- Any non-zero 64-bit signed integer is valid.
Default: `1`.

Note: When Snowflake reserves the next `n` values for a single request, the actual values returned may not be contiguous across concurrent sessions.

### `ORDER | NOORDER`
Controls whether values are guaranteed to be returned in strict ascending order.

- `ORDER`: Guarantees monotonically increasing values. Has a concurrency performance cost.
- `NOORDER` (typical default): Values are unique but not guaranteed to be issued in ascending order across concurrent sessions. Better performance for high-throughput insert workloads.

The account-level `NOORDER_SEQUENCE_AS_DEFAULT` parameter controls which behavior is the default when neither is specified.

### `COMMENT = '<string_literal>'`
Free-text description of the sequence. Visible in `SHOW SEQUENCES` output and the Snowsight UI.

## Key Behavioral Notes

- Snowflake does **not** guarantee gap-free sequences. Values may be skipped due to transaction rollbacks, reserved-but-unused batches, or node failures. Do not rely on sequences for gapless numbering.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive; never use both in the same statement.
- Sequences can be used in `DEFAULT` column expressions: `DEFAULT my_seq.NEXTVAL`.
- To reference the sequence in a DML statement: `SELECT my_seq.NEXTVAL` or use it as a column default.
- Sequences maintain state across sessions and transactions; there is no way to "reset" a sequence to a previous value without recreating it.
