# Snowflake Naming Convention Rules

## Databases
- Format: `UPPER_SNAKE_CASE`
- Include environment suffix: `_DEV`, `_STAGING`, `_PROD`
- Example: `SALES_DB_PROD`, `ANALYTICS_DB_DEV`

## Schemas
- Format: `lower_snake_case`
- Group by data layer: `raw`, `staging`, `mart`, `archive`
- Example: `raw_ingest`, `staging_orders`, `mart_finance`

## Tables
- Format: `UPPER_SNAKE_CASE`
- Prefix with domain: `SALES_`, `HR_`, `FINANCE_`, `OPS_`
- Example: `SALES_ORDERS`, `HR_EMPLOYEES`, `FINANCE_INVOICES`

## Views
- Format: `UPPER_SNAKE_CASE`
- Suffix with `_VW`
- Example: `SALES_ORDERS_VW`, `HR_HEADCOUNT_VW`

## Materialized Views
- Format: `UPPER_SNAKE_CASE`
- Suffix with `_MVW`
- Example: `FINANCE_DAILY_REVENUE_MVW`

## Stages
- Format: `lower_snake_case`
- Prefix with source system: `s3_`, `azure_`, `gcs_`
- Example: `s3_raw_orders`, `azure_hr_exports`

## Tasks
- Format: `UPPER_SNAKE_CASE`
- Suffix with `_TASK`
- Example: `REFRESH_SALES_MART_TASK`, `ARCHIVE_OLD_RECORDS_TASK`

## Streams
- Format: `UPPER_SNAKE_CASE`
- Suffix with `_STREAM`
- Example: `SALES_ORDERS_STREAM`, `HR_CHANGES_STREAM`

## Stored Procedures
- Format: `UPPER_SNAKE_CASE`
- Prefix with `SP_`
- Example: `SP_REFRESH_SALES_MART`, `SP_ARCHIVE_RECORDS`

## UDFs
- Format: `lower_snake_case`
- Prefix with `fn_`
- Example: `fn_calculate_tax`, `fn_format_phone_number`

## Warehouses
- Format: `UPPER_SNAKE_CASE`
- Suffix with `_WH`
- Group by team or workload: `ANALYTICS_WH`, `LOADING_WH`, `REPORTING_WH`
