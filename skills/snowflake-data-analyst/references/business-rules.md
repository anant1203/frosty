            # Business Rules for DATA_ANALYST
            # Auto-generated draft for BANKING_DB.BRONZE_LAYER
            # Review each section and replace placeholder comments with your real definitions.

            ---

            ## Metric Definitions

            Define what each business term means in SQL terms.

            <!-- Inferred from column names and types. Replace with your actual definitions. -->

<!-- - **AMOUNT** (TRANSACTIONS): SUM(TRANSACTIONS.AMOUNT) [add WHERE filters if needed] -->

            ---

            ## Canonical Date Columns

            Specify which date column to use for time-based filters per table.

            <!-- Inferred from DATE/TIMESTAMP columns. Mark the primary date per table. -->

<!-- - ACCOUNTS: use OPEN_DATE ← recommended primary -->
<!-- - TRANSACTIONS: use TRANSACTION_DATE ← recommended primary -->

            ---

            ## Standard Filters

            Filters applied to every query on a table unless the user says otherwise.

            <!-- Inferred status/categorical columns — add standard filters below. -->

<!-- - ACCOUNTS.ACCOUNT_TYPE: WHERE ACCOUNT_TYPE = '?' -->
<!-- - TRANSACTIONS.TRANSACTION_TYPE: WHERE TRANSACTION_TYPE = '?' -->

            ---

            ## Common Table Joins

            Canonical join keys between tables.

            <!-- Inferred from _ID columns appearing in multiple tables. Verify join direction. -->

<!-- - ACCOUNTS → TRANSACTIONS: JOIN ON ACCOUNTS.ACCOUNT_ID = TRANSACTIONS.ACCOUNT_ID -->
<!-- - ACCOUNTS → CUSTOMERS: JOIN ON ACCOUNTS.CUSTOMER_ID = CUSTOMERS.CUSTOMER_ID -->

            ---

            ## Column Aliases / Semantic Mappings

            Map plain-English terms to actual columns or expressions.

            <!-- Examples:
            - "revenue" → SUM(ORDER_VALUE) WHERE STATUS = 'COMPLETED'
            - "headcount" → COUNT(DISTINCT EMPLOYEE_ID) in HR_EMPLOYEES
            -->

            ---

            ## Business Calendar Rules

            Non-standard date or period logic.

            <!-- Examples:
            - Fiscal year starts February 1
            - "Last quarter" means the previous fiscal quarter
            -->
