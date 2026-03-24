# CREATE WAREHOUSE — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-warehouse

## Full Syntax

```sql
CREATE [ OR REPLACE ] WAREHOUSE [ IF NOT EXISTS ] <name>
       [ [ WITH ] objectProperties ]
       [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
       [ objectParams ]
```

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the warehouse within the account. Must start with an alphabetic character. Special characters require double-quoting. |

## Object Properties Defaults Table

| Parameter | Default |
|-----------|---------|
| `WAREHOUSE_TYPE` | STANDARD |
| `WAREHOUSE_SIZE` | XSMALL |
| `GENERATION` | '1' |
| `RESOURCE_CONSTRAINT` | MEMORY_16X (Snowpark-optimized only) |
| `MAX_CLUSTER_COUNT` | 1 |
| `MIN_CLUSTER_COUNT` | 1 |
| `SCALING_POLICY` | STANDARD |
| `AUTO_SUSPEND` | 600 (seconds) |
| `AUTO_RESUME` | TRUE |
| `INITIALLY_SUSPENDED` | FALSE |
| `RESOURCE_MONITOR` | None |
| `COMMENT` | None |
| `ENABLE_QUERY_ACCELERATION` | FALSE |
| `QUERY_ACCELERATION_MAX_SCALE_FACTOR` | 8 |

## Object Properties — Detailed Descriptions

**`WAREHOUSE_TYPE = STANDARD | 'SNOWPARK-OPTIMIZED'`**
Selects the warehouse type.
- STANDARD: General-purpose virtual warehouse for SQL queries and DML. Default.
- 'SNOWPARK-OPTIMIZED': Larger memory-per-node ratio for Snowpark (Python/Java/Scala) workloads and ML training. Requires quoting the value.

**`WAREHOUSE_SIZE = XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE | X5LARGE | X6LARGE`**
Controls the number of compute servers per cluster, and thus credit consumption rate. Each step up roughly doubles credits per hour. Default: XSMALL.

**`GENERATION = '1' | '2'`**
Selects the hardware generation for STANDARD warehouses. Generation 2 offers improved price-performance on supported cloud regions. Cannot be combined with memory-based RESOURCE_CONSTRAINT values. Default: '1'.

**`RESOURCE_CONSTRAINT = STANDARD_GEN_1 | STANDARD_GEN_2 | MEMORY_1X | MEMORY_1X_x86 | MEMORY_16X | MEMORY_16X_x86 | MEMORY_64X | MEMORY_64X_x86`**
Applies only to Snowpark-optimized warehouses. Specifies the memory-per-node profile. Default for Snowpark-optimized: MEMORY_16X.

**`MAX_CLUSTER_COUNT = <integer>`**
Maximum number of clusters in a multi-cluster warehouse. Value range: 1 to the account's upper limit. Setting MAX_CLUSTER_COUNT > 1 enables multi-cluster mode. Default: 1 (single-cluster).

**`MIN_CLUSTER_COUNT = <integer>`**
Minimum number of clusters that remain running even when idle. Must be ≤ MAX_CLUSTER_COUNT. Setting MIN_CLUSTER_COUNT = MAX_CLUSTER_COUNT creates a fixed-size multi-cluster warehouse. Default: 1.

**`SCALING_POLICY = STANDARD | ECONOMY`**
Controls how aggressively new clusters are started (multi-cluster only).
- STANDARD: Starts new clusters as soon as queuing is detected. Prioritises performance.
- ECONOMY: Waits until existing clusters are fully saturated before starting new ones. Prioritises cost.
Default: STANDARD.

**`AUTO_SUSPEND = <integer> | NULL`**
Seconds of inactivity after which the warehouse is automatically suspended. Set to 0 or NULL to disable auto-suspend (not recommended for cost control). Default: 600 seconds (10 minutes).

**`AUTO_RESUME = TRUE | FALSE`**
When TRUE, the warehouse automatically resumes when a query is submitted. When FALSE, the warehouse must be manually resumed. Default: TRUE.

**`INITIALLY_SUSPENDED = TRUE | FALSE`**
When TRUE, the warehouse is created in a suspended state and no compute nodes are provisioned until the warehouse is explicitly resumed or a query triggers AUTO_RESUME. Useful for pre-creating warehouses without immediate cost. Default: FALSE.

**`RESOURCE_MONITOR = <string>`**
Name of an existing resource monitor to assign to this warehouse for credit-usage tracking and alerting. Default: none (account-level monitor applies if set).

**`COMMENT = '<string_literal>'`**
Free-text description of the warehouse's purpose or owning team. Default: none.

**`ENABLE_QUERY_ACCELERATION = TRUE | FALSE`**
Enables the Query Acceleration Service for eligible queries, offloading portions of large scan workloads to shared serverless compute. Default: FALSE.

**`QUERY_ACCELERATION_MAX_SCALE_FACTOR = <integer>`**
Maximum scale factor (0–100) for the Query Acceleration Service. 0 means unlimited scaling. Only relevant when ENABLE_QUERY_ACCELERATION = TRUE. Default: 8.

## Object Parameters Defaults Table

| Parameter | Default |
|-----------|---------|
| `MAX_CONCURRENCY_LEVEL` | 8 |
| `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS` | 0 (no timeout) |
| `STATEMENT_TIMEOUT_IN_SECONDS` | 172800 (48 hours) |

## Object Parameters — Detailed Descriptions

**`MAX_CONCURRENCY_LEVEL = <integer>`**
Maximum number of SQL statements that can execute concurrently in the warehouse. Statements beyond this limit are queued. Default: 8.

**`STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <integer>`**
Maximum number of seconds a statement may wait in the queue before being cancelled. 0 disables the timeout (statements wait indefinitely). Default: 0.

**`STATEMENT_TIMEOUT_IN_SECONDS = <integer>`**
Maximum number of seconds a statement may execute before being cancelled. Default: 172800 (48 hours).

## Tags

```sql
[ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] )
```

Tag values are strings; maximum 256 characters per value.

## Behavioral Notes

- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.
- Creating a warehouse automatically sets it as the active warehouse for the current session.
- Initial provisioning of nodes may take a few seconds; creating in INITIALLY_SUSPENDED state avoids this latency.
- Multi-cluster mode (MAX_CLUSTER_COUNT > 1) requires Snowflake Enterprise Edition or higher.

## Access Control Requirements

The `CREATE WAREHOUSE` privilege on the account is required. By default only SYSADMIN or higher has this privilege.
