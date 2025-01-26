import os
from helpers import connect_to_snowflake, execute_queries

def get_static_queries() -> list[str]:
    """Generate SQL queries for Snowflake RBAC setup.
    
    Returns:
        list[str]: A list of SQL queries that:
        - Create databases, warehouses, and roles
        - Set up permissions for LOADER, TRANSFORMER, ANALYZER, and MONITOR roles
        - Create users and assign roles
        - Configure role hierarchy and admin privileges
    """
    # Define databases using environment variables
    raw_database = os.getenv('SNOWFLAKE_RAW_DATABASE')
    development_database = os.getenv('SNOWFLAKE_DEVELOPMENT_DATABASE')
    pr_database = os.getenv('SNOWFLAKE_PR_DATABASE')  # PR database is used as BETA
    production_database = os.getenv('SNOWFLAKE_PRODUCTION_DATABASE')
    
    environment_databases = [development_database, pr_database, production_database]
    all_databases = [raw_database] + environment_databases
    
    # Define roles
    roles = ["LOADER_ROLE", "TRANSFORMER_ROLE", "ANALYZER_ROLE", "MONITOR_ROLE"]

    return [
        # Database Creation
        *[f"CREATE DATABASE IF NOT EXISTS {db};" for db in all_databases],

        # Drop public schemas
        *[f"USE DATABASE {db};" for db in all_databases],
        *[f"DROP SCHEMA IF EXISTS PUBLIC CASCADE;" for db in all_databases],

        # Warehouse Creation
        """CREATE WAREHOUSE IF NOT EXISTS X_SMALL_WH WITH
            WAREHOUSE_SIZE = 'xsmall'
            AUTO_SUSPEND = 60
            AUTO_RESUME = true
            INITIALLY_SUSPENDED = true;""",

        # Role Creation
        *[f"CREATE ROLE IF NOT EXISTS {role};" for role in roles],

        # LOADER_ROLE Grants
        "GRANT USAGE ON WAREHOUSE X_SMALL_WH TO ROLE LOADER_ROLE;",
        f"GRANT USAGE ON DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT CREATE SCHEMA ON DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT CREATE TABLE ON ALL SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT CREATE VIEW ON ALL SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT SELECT, REFERENCES ON ALL VIEWS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT CREATE TABLE ON FUTURE SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT CREATE VIEW ON FUTURE SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT SELECT, REFERENCES ON FUTURE VIEWS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT OWNERSHIP ON DATABASE {raw_database} TO ROLE LOADER_ROLE COPY CURRENT GRANTS;",
        f"GRANT OWNERSHIP ON ALL SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE COPY CURRENT GRANTS;",
        f"GRANT OWNERSHIP ON ALL TABLES IN DATABASE {raw_database} TO ROLE LOADER_ROLE COPY CURRENT GRANTS;",
        f"GRANT OWNERSHIP ON ALL VIEWS IN DATABASE {raw_database} TO ROLE LOADER_ROLE COPY CURRENT GRANTS;",
        f"GRANT OWNERSHIP ON FUTURE SCHEMAS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT OWNERSHIP ON FUTURE TABLES IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",
        f"GRANT OWNERSHIP ON FUTURE VIEWS IN DATABASE {raw_database} TO ROLE LOADER_ROLE;",

        # TRANSFORMER_ROLE Grants
        "GRANT USAGE ON WAREHOUSE X_SMALL_WH TO ROLE TRANSFORMER_ROLE;",
        # All databases - basic usage
        *[f"GRANT USAGE ON DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in all_databases],
        *[f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in all_databases],
        *[f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON ALL TABLES IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON ALL VIEWS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON FUTURE TABLES IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON FUTURE VIEWS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in all_databases],
        
        # Additional permissions for environment databases only
        *[f"GRANT CREATE SCHEMA ON DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT CREATE TABLE ON ALL SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT CREATE VIEW ON ALL SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT REFERENCES ON ALL VIEWS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT CREATE TABLE ON FUTURE SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT CREATE VIEW ON FUTURE SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT REFERENCES ON FUTURE VIEWS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT OWNERSHIP ON DATABASE {db} TO ROLE TRANSFORMER_ROLE COPY CURRENT GRANTS;" for db in environment_databases],
        *[f"GRANT OWNERSHIP ON ALL SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE COPY CURRENT GRANTS;" for db in environment_databases],
        *[f"GRANT OWNERSHIP ON ALL TABLES IN DATABASE {db} TO ROLE TRANSFORMER_ROLE COPY CURRENT GRANTS;" for db in environment_databases],
        *[f"GRANT OWNERSHIP ON ALL VIEWS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE COPY CURRENT GRANTS;" for db in environment_databases],
        *[f"GRANT OWNERSHIP ON FUTURE SCHEMAS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT OWNERSHIP ON FUTURE TABLES IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],
        *[f"GRANT OWNERSHIP ON FUTURE VIEWS IN DATABASE {db} TO ROLE TRANSFORMER_ROLE;" for db in environment_databases],

        # ANALYZER_ROLE Grants
        "GRANT USAGE ON WAREHOUSE X_SMALL_WH TO ROLE ANALYZER_ROLE;",
        *[f"GRANT USAGE ON DATABASE {db} TO ROLE ANALYZER_ROLE;" for db in all_databases],
        *[f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {db} TO ROLE ANALYZER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON ALL TABLES IN DATABASE {db} TO ROLE ANALYZER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON ALL VIEWS IN DATABASE {db} TO ROLE ANALYZER_ROLE;" for db in all_databases],
        *[f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {db} TO ROLE ANALYZER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON FUTURE TABLES IN DATABASE {db} TO ROLE ANALYZER_ROLE;" for db in all_databases],
        *[f"GRANT SELECT ON FUTURE VIEWS IN DATABASE {db} TO ROLE ANALYZER_ROLE;" for db in all_databases],

        # MONITOR_ROLE Grants
        "GRANT MONITOR ON WAREHOUSE X_SMALL_WH TO ROLE MONITOR_ROLE;",
        *[f"GRANT USAGE ON DATABASE {db} TO ROLE MONITOR_ROLE;" for db in all_databases],
        *[f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {db} TO ROLE MONITOR_ROLE;" for db in all_databases],

        # User Creation and Role Grants
        f"""CREATE USER IF NOT EXISTS {os.getenv('SNOWFLAKE_GITHUB_USER')}
            PASSWORD = '{os.getenv('SNOWFLAKE_GITHUB_PASSWORD')}'
            LOGIN_NAME = '{os.getenv('SNOWFLAKE_GITHUB_USER')}'
            MUST_CHANGE_PASSWORD = false
            DEFAULT_WAREHOUSE = 'X_SMALL_WH'
            DEFAULT_ROLE = 'LOADER_ROLE';""",
        f"GRANT ROLE LOADER_ROLE TO USER {os.getenv('SNOWFLAKE_GITHUB_USER')};",

        f"""CREATE USER IF NOT EXISTS {os.getenv('SNOWFLAKE_DBT_USER')}
            PASSWORD = '{os.getenv('SNOWFLAKE_DBT_PASSWORD')}'
            LOGIN_NAME = '{os.getenv('SNOWFLAKE_DBT_USER')}'
            MUST_CHANGE_PASSWORD = false
            DEFAULT_WAREHOUSE = 'X_SMALL_WH'
            DEFAULT_ROLE = 'TRANSFORMER_ROLE';""",
        f"GRANT ROLE TRANSFORMER_ROLE TO USER {os.getenv('SNOWFLAKE_DBT_USER')};",

        f"""CREATE USER IF NOT EXISTS {os.getenv('SNOWFLAKE_HEX_USER')}
            PASSWORD = '{os.getenv('SNOWFLAKE_HEX_PASSWORD')}'
            LOGIN_NAME = '{os.getenv('SNOWFLAKE_HEX_USER')}'
            MUST_CHANGE_PASSWORD = false
            DEFAULT_WAREHOUSE = 'X_SMALL_WH'
            DEFAULT_ROLE = 'ANALYZER_ROLE';""",
        f"GRANT ROLE ANALYZER_ROLE TO USER {os.getenv('SNOWFLAKE_HEX_USER')};",

        # Role Hierarchy
        *[f"GRANT ROLE {role} TO ROLE SYSADMIN;" for role in roles],

        # Fix ACCOUNTADMIN and SYSADMIN grants
        *[f"GRANT ALL PRIVILEGES ON DATABASE {db} TO ROLE {role};" 
          for role in ['ACCOUNTADMIN', 'SYSADMIN'] 
          for db in all_databases],
        *[f"GRANT ALL PRIVILEGES ON ALL SCHEMAS IN DATABASE {db} TO ROLE {role};" 
          for role in ['ACCOUNTADMIN', 'SYSADMIN'] 
          for db in all_databases],
        *[f"GRANT ALL PRIVILEGES ON ALL TABLES IN DATABASE {db} TO ROLE {role};" 
          for role in ['ACCOUNTADMIN', 'SYSADMIN'] 
          for db in all_databases],
        *[f"GRANT ALL PRIVILEGES ON ALL VIEWS IN DATABASE {db} TO ROLE {role};" 
          for role in ['ACCOUNTADMIN', 'SYSADMIN'] 
          for db in all_databases],
        *[f"GRANT ALL PRIVILEGES ON FUTURE SCHEMAS IN DATABASE {db} TO ROLE {role};" 
          for role in ['ACCOUNTADMIN', 'SYSADMIN'] 
          for db in all_databases],
        *[f"GRANT ALL PRIVILEGES ON FUTURE TABLES IN DATABASE {db} TO ROLE {role};" 
          for role in ['ACCOUNTADMIN', 'SYSADMIN'] 
          for db in all_databases],
        *[f"GRANT ALL PRIVILEGES ON FUTURE VIEWS IN DATABASE {db} TO ROLE {role};" 
          for role in ['ACCOUNTADMIN', 'SYSADMIN'] 
          for db in all_databases],
    ]

def main() -> None:
    """Execute the Snowflake RBAC setup process.
    
    Connects to Snowflake, executes all setup queries, and closes the connection.
    Prints progress messages to stdout.
    """
    print("\nConnecting to Snowflake...")
    conn = connect_to_snowflake()
    print("Successfully connected to Snowflake")
    
    print("\nExecuting setup queries...")
    queries = get_static_queries()
    execute_queries(conn, queries)
    
    print("\nSetup completed")
    conn.close()
    print("Connection closed")


main()