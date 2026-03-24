# CREATE COMPUTE POOL — Parameter Reference

Source: https://docs.snowflake.com/en/sql-reference/sql/create-compute-pool

## Full Syntax

```sql
CREATE COMPUTE POOL [ IF NOT EXISTS ] <name>
  [ FOR APPLICATION <app_name> ]
  MIN_NODES = <num>
  MAX_NODES = <num>
  INSTANCE_FAMILY = <instance_family_name>
  [ AUTO_RESUME = { TRUE | FALSE } ]
  [ INITIALLY_SUSPENDED = { TRUE | FALSE } ]
  [ AUTO_SUSPEND_SECS = <num> ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
  [ PLACEMENT_GROUP = '<placement_group_name>' ]
```

Note: `CREATE OR REPLACE` is not supported for compute pools. Use `CREATE COMPUTE POOL IF NOT EXISTS` to avoid errors on re-runs.

## Required Parameters

| Parameter | Description |
|-----------|-------------|
| `<name>` | Unique identifier for the compute pool within the account. Must be unquoted (quoted or case-sensitive names are not permitted). |
| `MIN_NODES = <num>` | Minimum number of nodes the pool maintains. Must be greater than 0. The pool will never scale below this count. |
| `MAX_NODES = <num>` | Maximum number of nodes the pool may scale up to. Must be ≥ MIN_NODES. |
| `INSTANCE_FAMILY = <instance_family_name>` | The machine type (hardware profile) for all nodes in the pool. Determines CPU, memory, GPU, and credit consumption rate. Cannot be changed after creation. |

## Optional Parameters Defaults Table

| Parameter | Default |
|-----------|---------|
| `FOR APPLICATION` | None (pool is account-scoped, not app-restricted) |
| `AUTO_RESUME` | TRUE |
| `INITIALLY_SUSPENDED` | FALSE |
| `AUTO_SUSPEND_SECS` | 3600 (1 hour) |
| `TAG` | None |
| `COMMENT` | None |
| `PLACEMENT_GROUP` | None |

## Optional Parameters — Detailed Descriptions

**`FOR APPLICATION <app_name>`**
Restricts the compute pool so it can only be used by the specified Snowflake Native App. Once set, this restriction cannot be changed. Omit for general-purpose pools.

**`AUTO_RESUME = TRUE | FALSE`**
When TRUE (default), if a new service is submitted to a suspended compute pool, Snowflake automatically resumes the pool before starting the service. When FALSE, the pool must be manually resumed via `ALTER COMPUTE POOL <name> RESUME` before services can run on it.

**`INITIALLY_SUSPENDED = TRUE | FALSE`**
When TRUE, the compute pool is created in a suspended state; no nodes are provisioned and no credits are consumed until the pool is resumed. Recommended for pools that will not be used immediately. Default: FALSE (nodes provisioned on creation).

**`AUTO_SUSPEND_SECS = <num>`**
Number of seconds of inactivity (no running services) after which Snowflake automatically suspends the compute pool and stops billing. Must be a positive integer. Default: 3600 seconds (1 hour). Set lower to reduce idle costs; set higher for pools that must start quickly for frequent intermittent workloads.

**`TAG ( <tag_name> = '<tag_value>' [ , ... ] )`**
Assigns object tag name-value pairs to the compute pool for cost attribution and governance. Tag values are strings; maximum 256 characters per value.

**`COMMENT = '<string_literal>'`**
Free-text description of the compute pool's purpose, owning team, or associated workload. Default: none.

**`PLACEMENT_GROUP = '<placement_group_name>'`**
Assigns the compute pool to a named placement group, controlling the physical proximity of nodes.
- Use a specific named group for low-latency, tightly-coupled distributed workloads.
- Use `'DISTRIBUTED'` to spread nodes across multiple placement groups for improved fault tolerance.
Default: none (Snowflake determines placement).

## INSTANCE_FAMILY Valid Values

### CPU-Based (General Purpose)
| Value | vCPUs | Memory | Notes |
|-------|-------|--------|-------|
| CPU_X64_XS | 2 | 8 GB | Extra-small; lightweight tasks |
| CPU_X64_S | 4 | 16 GB | Small general-purpose |
| CPU_X64_M | 8 | 32 GB | Medium general-purpose |
| CPU_X64_L | 32 | 128 GB | Large general-purpose |

### High-Memory
| Value | vCPUs | Memory | Notes |
|-------|-------|--------|-------|
| HIGHMEM_X64_S | 8 | 64 GB | High memory / data-intensive |
| HIGHMEM_X64_M | 32 | 256 GB | Large high-memory |
| HIGHMEM_X64_L | 128 | 1 TB | Extra-large high-memory |

### GPU-Enabled
| Value | GPU | Notes |
|-------|-----|-------|
| GPU_NV_S | 1x NVIDIA A10G | Single-GPU inference/light training |
| GPU_NV_M | 4x NVIDIA A10G | Multi-GPU training |
| GPU_NV_L | 8x NVIDIA A100 | Large-scale GPU training |

Availability of specific instance families varies by cloud provider (AWS, Azure, GCP) and region. Consult the Snowflake documentation for your region's supported families.

## Behavioral Notes

- `CREATE OR REPLACE` is not supported; use `IF NOT EXISTS`.
- INSTANCE_FAMILY cannot be altered after the pool is created; a new pool must be created to change it.
- MIN_NODES and MAX_NODES can be updated via `ALTER COMPUTE POOL`.
- Compute pools are a Snowpark Container Services feature and require the appropriate Snowflake edition and region support.
- A service submitted to a suspended pool with AUTO_RESUME = TRUE will wait for the pool to resume (may take several minutes depending on instance type).

## Access Control Requirements

The `CREATE COMPUTE POOL` privilege on the account is required. By default only ACCOUNTADMIN or a role granted this privilege can create compute pools.
