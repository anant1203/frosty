---
name: snowflake-create-network-rule
description: Consult Snowflake CREATE NETWORK RULE parameter reference before generating any CREATE NETWORK RULE DDL.
---

Before writing a CREATE NETWORK RULE statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — use `CREATE NETWORK RULE` (IF NOT EXISTS is not supported for this object).
5. TYPE and MODE must always be specified — they are required parameters with no implicit defaults in the DDL.
6. Match TYPE to MODE correctly: INGRESS rules use IPV4, AWSVPCEID, AZURELINKID, or GCPPSCID; EGRESS rules use HOST_PORT or PRIVATE_HOST_PORT; INTERNAL_STAGE requires AWSVPCEID.
7. VALUE_LIST entries must match the chosen TYPE format (CIDR for IPV4, domain[:port] for HOST_PORT, etc.).
