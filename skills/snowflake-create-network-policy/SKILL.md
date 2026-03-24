---
name: snowflake-create-network-policy
description: Consult Snowflake CREATE NETWORK POLICY parameter reference before generating any CREATE NETWORK POLICY DDL.
---

Before writing a CREATE NETWORK POLICY statement:
1. Read `references/parameters.md` to review all available parameters and their defaults.
2. For each parameter, decide whether the user's request implies a non-default value.
3. Include only the parameters that differ from the default or that the user explicitly requested.
4. Never use `CREATE OR REPLACE` — always use `CREATE NETWORK POLICY IF NOT EXISTS`.
5. Prefer ALLOWED_NETWORK_RULE_LIST and BLOCKED_NETWORK_RULE_LIST (referencing named NETWORK RULEs) over the legacy ALLOWED_IP_LIST / BLOCKED_IP_LIST parameters.
6. Remind the user that a network policy has no effect until it is attached via `ALTER ACCOUNT SET NETWORK_POLICY`, `ALTER USER SET NETWORK_POLICY`, or `ALTER INTEGRATION SET NETWORK_POLICY`.
7. BLOCKED_IP_LIST is evaluated before ALLOWED_IP_LIST; entries in both lists result in the IP being blocked.
