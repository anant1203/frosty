class Privilege():
    _allowed_object_type = ["USER","ROLE","WAREHOUSE","DATABASE","SCHEMA","TABLE",
    "FILEFORMAT","PIPE","TASK","STAGE","STREAM","RESOURCEMONITOR","EXTERNALVOLUME","FAILOVERGROUP","REPLICATIONGROUP",
    "INTEGRATION","AUTHENTICATIONPOLICY","NETWORKRULE","NETWORKPOLICY","PACKAGESPOLICY","PASSWORDPOLICY","PROVISIONEDTHROUGHPUT",
    "SESSIONPOLICY","DATAEXCHANGE","LISTING","ORGANIZATIONPROFILE","CORTEXSEARCHSERVICE","CONNECTION","DYNAMICTABLE","EVENTTABLE",
    "EXTERNALTABLE","HYBRIDTABLE","ICEBERGTABLE","VIEW","MATERIALIZEDVIEW","SEMANTICVIEW","NOTEBOOK","DATABASEROLE","SECRET","AGGREGATIONPOLICY",
    "JOINPOLICY","MASKINGPOLICY","PRIVACYPOLICY","PROJECTIONPOLICY","ROWACCESSPOLICY","TAG","SEQUENCE","STOREDPROCEDURE","USERDEFINEDFUNCTION",
    "EXTERNALFUNCTION","DATAMETRICFUNCTION","ALERT","COMPUTEPOOL","IMAGEREPOSITORY","SERVICE","SNAPSHOT","SNAPSHOTPOLICY","SNAPSHOTSET",
    "STREAMLIT","MODEL","APPLICATIONPACKAGE","CONTACT","DATASET"]

    _allowed_privileges = {
        "USER": {"MONITOR":"Grants the ability to view the login history for the user.",
                 "OWNERSHIP":"Grants full control over a user/role. Only a single role can hold this privilege on a specific object at a time.",
                 "ALL":"Grants all privileges, except OWNERSHIP, on the user.",
                 "IMPERSONATE":"Runs a task on behalf of a specified user account.",
                 "MODIFY PROGRAMMATIC AUTHENTICATION METHODS":"Grants the ability to create, modify, delete, rotate, and view information about the programmatic access tokens and key pairs for the user."},
        "ROLE": {
            "OWNERSHIP": "Grants full control over a role. Only a single role can hold this privilege on a specific object at a time."
        },
        "STAGE": {
            "USAGE":"Enables using an external stage object in a SQL statement and includes the READ and WRITE privileges; not applicable to internal stages.",
            "READ":"Enables performing any operations that require reading from a stage (for example, file staging commands and COPY INTO <table>).",
            "WRITE":"Enables performing any operations that require writing to a stage (for example, file staging commands and COPY INTO <location>).",
            "OWNERSHIP":"Grants full control over the stage. Only a single role can hold this privilege on a specific object at a time. Note that in a managed access schema, only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants.",
            "ALL":"Grants all applicable privileges, except OWNERSHIP, on the stage (internal or external)."
        },
        "WAREHOUSE": {
            "APPLYBUDGET": "Enables adding or removing a warehouse from a budget.",
            "MODIFY": "Enables altering any properties of a warehouse, including changing its size. Required to assign a warehouse to a resource monitor. Note that only the ACCOUNTADMIN role can assign warehouses to resource monitors.",
            "MONITOR": "Enables viewing current and past queries executed on a warehouse as well as usage statistics on that warehouse.",
            "OPERATE": "Enables changing the state of a warehouse (stop, start, suspend, resume). In addition, enables viewing current and past queries executed on a warehouse and aborting any executing queries.",
            "USAGE": "Enables using a virtual warehouse and, as a result, executing queries on the warehouse. If the warehouse is configured to auto-resume when a SQL statement (e.g. query) is submitted to it, the warehouse resumes automatically and executes the statement.",
            "OWNERSHIP": "Grants full control over a warehouse. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the warehouse."
        },
        "DATABASE": {
            "APPLYBUDGET":"Enables adding or removing a database from a budget.",
            "MODIFY":"Enables altering any settings of a database.",
            "MONITOR":"Enables performing the DESCRIBE command on the database.",
            "USAGE":"Enables using a database, including returning the database details in the SHOW DATABASES command output. Additional privileges are required to view or take actions on objects in a database.",
            "REFERENCE_USAGE":"Enables using an object (e.g. secure view in a share) when the object references another object in a different database. Grant the privilege on the other database to the share. You cannot grant this privilege on a database to any kind of role. For details, see GRANT <privilege> … TO SHARE and Share data from multiple databases.",
            "CREATE DATABASE ROLE":"Enables creating a new database role in a database.",
            "CREATE SCHEMA":"Enables creating a new schema in a database, including cloning a schema.",
            "IMPORTED PRIVILEGES":"Enables roles other than the owning role to access a shared database; applies only to shared databases.",
            "OWNERSHIP":"Grants full control over the database. Only a single role can hold this privilege on a specific object at a time.",
            "ALL":"Grants all privileges, except OWNERSHIP, on a database.",
            "EXECUTE AUTO CLASSIFICATION":"Grants the ability to set a classification profile on a database in order to implement sensitive data classification."
        },
        "SCHEMA": {
            "APPLYBUDGET": "Enables adding or removing a schema from a budget.",
            "MODIFY": "Enables altering any settings of a schema.",
            "MONITOR": "Enables viewing schema details such as DESCRIBE output and basic metadata.",
            "USAGE": "Enables using a schema, including returning the schema details in the SHOW SCHEMAS command output.",
            "CREATE AUTHENTICATION POLICY": "Enables creating an authentication policy in the schema.",
            "CREATE DATA METRIC FUNCTION": "Enables creating a data metric function in the schema.",
            "CREATE TABLE": "Enables creating a new table in a schema, including cloning.",
            "CREATE DYNAMIC TABLE": "Enables creating a new dynamic table in a schema.",
            "CREATE EVENT TABLE": "Enables creating a new event table in a schema.",
            "CREATE EXTERNAL TABLE": "Enables creating a new external table in a schema.",
            "CREATE GIT REPOSITORY": "Enables creating a new Git repository stage in a schema.",
            "CREATE ICEBERG TABLE": "Enables creating a new Iceberg table in a schema.",
            "CREATE VIEW": "Enables creating a new view in a schema.",
            "CREATE MASKING POLICY": "Enables creating a masking policy in a schema.",
            "CREATE MATERIALIZED VIEW": "Enables creating a new materialized view in a schema.",
            "CREATE NETWORK RULE": "Enables creating a new network rule in a schema.",
            "CREATE NOTEBOOK": "Enables creating a new notebook in a schema.",
            "CREATE ROW ACCESS POLICY": "Enables creating a new row access policy in a schema.",
            "CREATE SECRET": "Enables creating a new secret in a schema.",
            "CREATE SESSION POLICY": "Enables creating a new session policy in a schema.",
            "CREATE STAGE": "Enables creating a new stage in a schema, including cloning.",
            "CREATE STREAMLIT": "Enables creating a new Streamlit app in a schema.",
            "CREATE FILE FORMAT": "Enables creating a new file format in a schema.",
            "CREATE SEQUENCE": "Enables creating a new sequence in a schema.",
            "CREATE FUNCTION": "Enables creating a new function in a schema.",
            "CREATE PACKAGES POLICY": "Enables creating a packages policy in a schema.",
            "CREATE PASSWORD POLICY": "Enables creating a password policy in a schema.",
            "CREATE PIPE": "Enables creating a new pipe in a schema.",
            "CREATE STREAM": "Enables creating a new stream in a schema.",
            "CREATE TAG": "Enables creating a new tag in a schema.",
            "CREATE TASK": "Enables creating a new task in a schema.",
            "CREATE PROCEDURE": "Enables creating a new stored procedure in a schema.",
            "CREATE ALERT": "Enables creating a new alert in a schema.",
            "CREATE CORTEX SEARCH SERVICE": "Enables creating a new Cortex Search service on a schema.",
            "CREATE SNOWFLAKE.CORE.BUDGET": "Enables creating a budget (SNOWFLAKE.CORE.BUDGET) in the schema.",
            "CREATE SNOWFLAKE.DATA_PRIVACY.CLASSIFICATION_PROFILE": "Enables creating a classification profile in the schema.",
            "CREATE SNOWFLAKE.DATA_PRIVACY.CUSTOM_CLASSIFIER": "Enables creating a custom classifier in the schema.",
            "CREATE SNOWFLAKE.ML.ANOMALY_DETECTION": "Enables creating an anomaly detection model build in the schema.",
            "CREATE SNOWFLAKE.ML.CLASSIFICATION": "Enables creating a classification model build in the schema.",
            "CREATE SNOWFLAKE.ML.FORECAST": "Enables creating a forecasting model build in the schema.",
            "CREATE SNOWFLAKE.ML.TOP_INSIGHTS": "Enables creating a Top Insights model build in the schema.",
            "CREATE SNOWFLAKE.ML.DOCUMENT_INTELLIGENCE": "Enables creating a Document AI model build in the schema.",
            "CREATE MODEL": "Enables creating a model in a schema.",
            "CREATE MODEL MONITOR": "Enables creating a model monitor in a schema.",
            "CREATE IMAGE REPOSITORY": "Enables creating an image repository in a schema.",
            "CREATE SERVICE": "Enables creating a service in a schema.",
            "CREATE SNAPSHOT": "Enables creating a snapshot in a schema.",
            "ADD SEARCH OPTIMIZATION": "Enables adding search optimization on objects in the schema.",
            "OWNERSHIP": "Grants full control over the schema. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a schema."
        },
        "TABLE": {
            "SELECT": "Enables executing a SELECT statement on a table and classifying a table.",
            "INSERT": "Enables executing an INSERT command on a table. Also enables using the ALTER TABLE command with a RECLUSTER clause to manually recluster a table with a clustering key.",
            "UPDATE": "Enables executing an UPDATE command on a table.",
            "TRUNCATE": "Enables executing a TRUNCATE TABLE command on a table.",
            "DELETE": "Enables executing a DELETE command on a table.",
            "EVOLVE SCHEMA": "Enables schema evolution to occur on a table when loading data.",
            "REFERENCES": "Enables referencing a table as the unique/primary key table for a foreign key constraint. Also enables viewing the structure of a table (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema.",
            "APPLYBUDGET": "Enables adding or removing a table from a budget.",
            "OWNERSHIP": "Grants full control over the table. Required to alter most properties of a table, with the exception of reclustering. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a table."
        },
        "FILEFORMAT": {
            "USAGE": "Enables using a file format in a SQL statement.",
            "OWNERSHIP": "Grants full control over the file format. Required to alter a file format. Only a single role can hold this privilege on a specific object at a time. Note that in a managed access schema, only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the file format."
        },
        "PIPE": {
            "APPLYBUDGET": "Enables adding or removing a pipe from a budget.",
            "MONITOR": "Enables viewing details for the pipe (using DESCRIBE PIPE or SHOW PIPES).",
            "OPERATE": "Enables viewing details for the pipe (using DESCRIBE PIPE or SHOW PIPES), pausing or resuming the pipe, and refreshing the pipe.",
            "OWNERSHIP": "Grants full control over the pipe. Only a single role can hold this privilege on a specific object at a time. Note that in a managed access schema, only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the pipe."
        },
        "STREAM": {
            "SELECT": "Enables executing a SELECT statement on a stream, which also allows you to view the stream in the output of the SHOW STREAMS command. To view the table_name and base_tables columns, you need at least one access privilege on the stream's source object.",
            "OWNERSHIP": "Grants full control over the stream. Only a single role can hold this privilege on a specific object at a time. Note that in a managed access schema, only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the stream."
        },
        "TASK": {
            "APPLYBUDGET": "Enables adding or removing a task from a budget.",
            "MONITOR": "Enables viewing details for the task (using DESCRIBE TASK or SHOW TASKS).",
            "OPERATE": "Enables viewing details for the task (using DESCRIBE TASK or SHOW TASKS) and resuming or suspending the task.",
            "OWNERSHIP": "Grants full control over the task. Only a single role can hold this privilege on a specific object at a time. Note that in a managed access schema, only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the task."
        },
        "RESOURCEMONITOR": {
            "MODIFY": "Enables altering any properties of a resource monitor, such as changing the monthly credit quota.",
            "MONITOR": "Enables viewing a resource monitor.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the resource monitor."
        },
        "EXTERNALVOLUME": {
            "USAGE": "Enables referencing the external volume when executing other commands that use the external volume, and grants the ability to view details for an external volume in a SHOW or DESCRIBE command.",
            "OWNERSHIP": "Grants full control over an external volume. Only a single role can hold this privilege on a specific object at a time."
        },
        "FAILOVERGROUP": {
            "MODIFY": "Enables altering any properties of a failover group.",
            "MONITOR": "Enables viewing details of a failover group.",
            "OWNERSHIP": "Grants full control over a failover group. Only a single role can hold this privilege on a specific object at a time.",
            "FAILOVER": "Enables promoting a secondary failover group to serve as primary failover group.",
            "REPLICATE": "Enables refreshing a secondary failover group.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the failover group."
        },
        "REPLICATIONGROUP": {
            "MODIFY": "Enables altering any properties of a replication group.",
            "MONITOR": "Enables viewing details of a replication group.",
            "OWNERSHIP": "Grants full control over a replication group. Only a single role can hold this privilege on a specific object at a time.",
            "REPLICATE": "Enables refreshing a secondary replication group.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the replication group."
        },
        "INTEGRATION": {
            "USAGE": "Enables referencing the integration when executing other commands that use the integration. For more information, see access control requirements for CREATE STAGE and CREATE EXTERNAL ACCESS INTEGRATION.",
            "USE_ANY_ROLE": "Allows the External OAuth client or user to switch roles only if this privilege is granted to the client or user. Configure the External OAuth security integration to use the EXTERNAL_OAUTH_ANY_ROLE_MODE parameter using CREATE SECURITY INTEGRATION or ALTER SECURITY INTEGRATION.",
            "OWNERSHIP": "Grants full control over an integration. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the integration."
        },
        "AUTHENTICATIONPOLICY": {
            "OWNERSHIP": "Grants full control over an authentication policy. Only a single role can hold this privilege on a specific object at a time."
        },
        "NETWORKRULE": {
            "OWNERSHIP": "Grants full control over a network rule. Only a single role can hold this privilege on a specific object at a time."
        },
        "NETWORKPOLICY": {
            "OWNERSHIP": "Grants full control over the network policy. Only a single role can hold this privilege on a specific object at a time.",
            "USAGE": "Grants the ability to apply a network policy."
        },
        "PACKAGESPOLICY": {
            "OWNERSHIP": "Transfers ownership of a packages policy, which grants full control over the packages policy. Required to alter most properties of a packages policy.",
            "USAGE": "Grants the ability to view the contents of a packages policy in a SHOW or DESCRIBE command."
        },
        "PASSWORDPOLICY": {
            "OWNERSHIP": "Grants full control over the password policy. Only a single role can hold this privilege on a specific object at a time."
        },
        "PROVISIONEDTHROUGHPUT": {
            "OWNERSHIP": "Grants full control over a provisioned throughput. Only one role at a time can hold this privilege on a specific object.",
            "USE": "Enables inference with a provisioned throughput.",
            "MONITOR": "Enables performing DESCRIBE and SHOW commands on a provisioned throughput."
        },
        "SESSIONPOLICY": {
            "OWNERSHIP": "Transfers ownership of a session policy, which grants full control over the session policy. Required to alter most properties of a session policy."
        },
        "DATAEXCHANGE": {
            "IMPORTED PRIVILEGES": "Enables roles other than the owning role to manage a Data Exchange."
        },
        "LISTING": {
            "MODIFY": "Enables roles other than the owning role to modify a listing.",
            "USAGE": "Enables viewing a listing.",
            "OWNERSHIP": "Grants full control over a listing. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a listing."
        },
        "ORGANIZATIONPROFILE": {
            "MODIFY": "Enables roles other than the owning role to modify an organization profile.",
            "OWNERSHIP": "Grants full control over an organization profile. Only a single role can hold this privilege on a specific object at a time."
        },
        "SHARE": {
            "OWNERSHIP": "Grants full control over a share. Only a single role can hold this privilege on a specific object at a time. Cannot be transferred."
        },
        "CORTEXSEARCH": {
            "OWNERSHIP": "Enables full control over the Cortex Search service. The role with this privilege can also remove a service from a schema.",
            "OPERATE": "Enables inspecting, suspending or resuming a Cortex Search service and modifying service properties.",
            "USAGE": "Enables invoking the service.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the service."
        },
        "CONNECTION": {
            "FAILOVER": "Grants the ability to promote a secondary connection to serve as the primary connection."
        },
        "DYNAMICTABLE": {
            "SELECT": "Enables executing a SELECT statement on a dynamic table. The SELECT privilege on a dynamic table allows you to view it in the output of the SHOW DYNAMIC TABLES command. If you have the SELECT privilege but don't have the MONITOR privilege, the following fields are hidden: text, warehouse, scheduling_state, last_suspended_on, and suspend_reason_code (only hidden in Snowsight).",
            "OPERATE": "Enables altering the properties of a dynamic table. If you do not have this privilege on a dynamic table, you can't use the ALTER DYNAMIC TABLE command (suspend, resume, refresh, SET warehouse/target lag). Additionally, lacking this privilege prevents executing CREATE DYNAMIC TABLE ... INITIALIZE = ON_CREATE to create a new dynamic table that consumes from it.",
            "MONITOR": "Enables accessing the metadata for a dynamic table through Snowsight and SQL commands/functions. While OPERATE grants this access and also allows altering dynamic tables, MONITOR is the more suitable option for roles that need read-only metadata access (for example, data scientists). With MONITOR you can call DYNAMIC_TABLE_GRAPH_HISTORY and DYNAMIC_TABLE_REFRESH_HISTORY, view the table in SHOW DYNAMIC TABLES, and view metadata via DESCRIBE DYNAMIC TABLE or Snowsight. If you have SELECT but not MONITOR, the fields text, warehouse, scheduling_state, last_suspended_on, and suspend_reason_code are hidden (Snowsight-only visibility).",
            "OWNERSHIP": "Grants full control over the dynamic table. Only a single role can hold this privilege on a specific object at a time. Required to drop a dynamic table.",
            "ALL": "Grants all privileges, except OWNERSHIP, on the dynamic table."
        },
        "EVENTTABLE": {
            "ALL": "Grants all privileges, except OWNERSHIP, on the event table.",
            "APPLYBUDGET": "Enables adding or removing an event table from a budget.",
            "DELETE": "Enables executing a DELETE command on an event table.",
            "OWNERSHIP": "Grants full control over the event table. Only a single role can hold this privilege on a specific object at a time.",
            "REFERENCES": "Enables referencing the event table in foreign key constraints and viewing its structure.",
            "SELECT": "Enables executing a SELECT statement on an event table.",
            "TRUNCATE": "Enables executing a TRUNCATE TABLE command on the event table."
        },
        "EXTERNALTABLE": {
            "SELECT": "Enables executing a SELECT statement on an external table and classifying an external table.",
            "REFERENCES": "Enables referencing the external table in foreign key constraints and viewing its structure.",
            "OWNERSHIP": "Grants full control over the external table. Required to refresh an external table. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on an external table."
        },
        "HYBRIDTABLE": {
            "SELECT": "Enables executing a SELECT statement on a hybrid table.",
            "INSERT": "Enables executing an INSERT command on a hybrid table.",
            "UPDATE": "Enables executing an UPDATE command on a hybrid table.",
            "TRUNCATE": "Enables executing a TRUNCATE TABLE command on a hybrid table.",
            "DELETE": "Enables executing a DELETE command on a hybrid table.",
            "REFERENCES": "Enables referencing a hybrid table in foreign key constraints and viewing its structure.",
            "APPLYBUDGET": "Enables adding or removing a hybrid table from a budget.",
            "OWNERSHIP": "Grants full control over the hybrid table. Required to alter most properties. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a hybrid table."
        },
        "ICEBERGTABLE": {
            "SELECT": "Enables executing a SELECT statement on an Iceberg table.",
            "INSERT": "Enables executing an INSERT command on an Iceberg table.",
            "UPDATE": "Enables executing an UPDATE command on an Iceberg table.",
            "TRUNCATE": "Enables executing a TRUNCATE TABLE command on an Iceberg table.",
            "DELETE": "Enables executing a DELETE command on an Iceberg table.",
            "REFERENCES": "Enables referencing an Iceberg table in foreign key constraints and viewing its structure.",
            "APPLYBUDGET": "Enables adding or removing an Iceberg table from a budget.",
            "OWNERSHIP": "Grants full control over an Iceberg table. Required to alter most properties. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on an Iceberg table."
        },

        "VIEW": {
            "SELECT": "Enables executing a SELECT statement on a view and classifying a view. This privilege is sufficient to query a view; the SELECT privilege is not required on the objects from which the view is created.",
            "REFERENCES": "Enables viewing the structure of a view (but not the data) via DESCRIBE or SHOW.",
            "OWNERSHIP": "Grants full control over the view. Required to alter a view. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a view."
        },
        "MATERIALIZEDVIEW": {
            "SELECT": "Enables executing a SELECT statement on a materialized view.",
            "REFERENCES": "Enables viewing the structure of a materialized view via DESCRIBE or SHOW.",
            "APPLYBUDGET": "Enables adding or removing a materialized view from a budget.",
            "OWNERSHIP": "Grants full control over a materialized view. Required to alter a materialized view. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a materialized view."
        },
        "SEMANTICVIEW": {
            "SELECT": "Enables executing a SELECT statement on a semantic view.",
            "REFERENCES": "Enables viewing the structure of a semantic view via DESCRIBE or SHOW.",
            "OWNERSHIP": "Grants full control over a semantic view. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a semantic view."
        },
        "NOTEBOOK": {
            "OWNERSHIP": "Grants full control over a notebook. Only a single role can hold this privilege on a specific object at a time.",
            "USAGE": "Enables creating and using a notebook in a schema."
        },
        "DATABASEROLE": {
            "OWNERSHIP": "Grants full control over a database role. Only a single role can hold this privilege on a specific object at a time."
        },
        "SECRET": {
            "READ": "Enables reading or retrieving a secret.",
            "USAGE": "Enables using a secret in operations.",
            "OWNERSHIP": "Grants full control over a secret. Only a single role can hold this privilege on a specific object at a time."
        },
        "AGGREGATIONPOLICY": {
            "APPLY": "Grants the ability to add and drop an aggregation policy on a table or view.",
            "OWNERSHIP": "Grants full control over an aggregation policy."
        },
        "JOINPOLICY": {
            "APPLY": "Grants the ability to add and drop a join policy on a table or view.",
            "OWNERSHIP": "Grants full control over a join policy."
        },

        "MASKINGPOLICY": {
            "APPLY": "Grants the ability to set a Column-level Security masking policy on a table or view column and to set a masking policy on a tag. This global privilege also allows executing the DESCRIBE operation on tables and views.",
            "OWNERSHIP": "Grants full control over a masking policy."
        },
        "PRIVACYPOLICY": {
            "APPLY": "Grants the ability to add and drop a privacy policy on a table or view.",
            "OWNERSHIP": "Grants full control over a privacy policy."
        },
        "PROJECTIONPOLICY": {
            "APPLY": "Grants the ability to add and drop a projection policy on a table or view.",
            "OWNERSHIP": "Grants full control over a projection policy."
        },
        "ROWACCESSPOLICY": {
            "APPLY": "Grants the ability to add and drop a row access policy on a table or view. This global privilege also allows executing the DESCRIBE operation on tables and views.",
            "OWNERSHIP": "Grants full control over a row access policy."
        },
        "TAG": {
            "APPLY": "Grants the ability to add or drop a tag on a Snowflake object.",
            "OWNERSHIP": "Grants full control over a tag. Only a single role can hold this privilege on a specific object at a time.",
            "READ": "Grants the ability to view tag metadata and read tag information."
        },
        "SEQUENCE": {
            "USAGE": "Enables using a sequence.",
            "OWNERSHIP": "Grants full control over a sequence. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a sequence."
        },
        "STOREDPROCEDURE": {
            "USAGE": "Enables executing a stored procedure.",
            "OWNERSHIP": "Grants full control over a stored procedure. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a stored procedure."
        },

        "USERDEFINEDFUNCTION": {
            "USAGE": "Enables executing a user-defined function.",
            "OWNERSHIP": "Grants full control over a user-defined function. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a user-defined function."
        },
        "EXTERNALFUNCTION": {
            "USAGE": "Enables invoking an external function.",
            "OWNERSHIP": "Grants full control over an external function. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on an external function."
        },
        "DATAMETRICFUNCTION": {
            "USAGE": "Enables executing a data metric function.",
            "OWNERSHIP": "Grants full control over a data metric function. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on a data metric function."
        },
        "ALERT": {
            "MONITOR": "Enables viewing and monitoring an alert.",
            "OPERATE": "Enables acting upon an alert (suspend, resume, or other operations depending on alert implementation).",
            "OWNERSHIP": "Grants full control over an alert. Only a single role can hold this privilege on a specific object at a time.",
            "ALL": "Grants all privileges, except OWNERSHIP, on an alert."
        },
        "COMPUTEPOOL": {
            "MONITOR": "Enables viewing the metadata and status for a compute pool.",
            "OPERATE": "Enables performing operational actions on a compute pool (suspend, resume, refresh, etc.).",
            "OWNERSHIP": "Grants full control over a compute pool. Only a single role can hold this privilege on a specific object at a time.",
            "MODIFY": "Enables modifying properties of a compute pool.",
            "USAGE": "Enables using a compute pool for workloads."
        },
        "IMAGEREPOSITORY": {
            "OWNERSHIP": "Grants full control over an image repository. Only a single role can hold this privilege on a specific object at a time.",
            "READ": "Enables reading or downloading images from the repository.",
            "WRITE": "Enables uploading images to the repository."
        },
        "SERVICE": {
            "OPERATE": "Enables operating the service (start, stop, suspend, resume and modify properties where applicable).",
            "OWNERSHIP": "Grants full control over the service. Only a single role can hold this privilege on a specific object at a time.",
            "MONITOR": "Enables viewing monitoring and usage information for the service."
        },

        "SNAPSHOT": {
            "OWNERSHIP": "Grants full control over a snapshot. Only a single role can hold this privilege on a specific object at a time.",
            "USAGE": "Enables referencing or using the snapshot in operations."
        },
        "SNAPSHOTPOLICY": {
            "OWNERSHIP": "Grants full control over a snapshot policy. Only a single role can hold this privilege on a specific object at a time.",
            "USAGE": "Enables using a snapshot policy in operations."
        },
        "SNAPSHOTSET": {
            "OWNERSHIP": "Grants full control over a snapshot set. Only a single role can hold this privilege on a specific object at a time.",
            "USAGE": "Enables using a snapshot set in operations."
        },
        "STREAMLIT": {
            "USAGE": "Enables creating and using a Streamlit app in a schema."
        },
        "MODEL": {
            "OWNERSHIP": "Grants full control over a model. Only a single role can hold this privilege on a specific object at a time.",
            "USAGE": "Enables invoking or using a model."
        },
        "APPLICATIONPACKAGE": {
            "ATTACH LISTING": "Enables attaching a listing to an application package."
        },
        "CONTACT": {
            "APPLY": "Enables applying contact-related changes.",
            "MODIFY": "Enables modifying contact information.",
            "OWNERSHIP": "Grants full control over a contact."
        },
        "DATASET": {
            "OWNERSHIP": "Grants full control over a dataset. Only a single role can hold this privilege on a specific object at a time.",
            "USAGE": "Enables using or accessing a dataset."
        }
    }
