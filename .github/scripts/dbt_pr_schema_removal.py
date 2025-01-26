import os
from helpers import connect_to_snowflake, execute_queries

def get_removal_queries(database: str, schema: str) -> list[str]:
    """Return SQL queries needed to tear down the specified schema.
    
    Args:
        database: Name of the Snowflake database
        schema: Name of the schema to be dropped
        
    Returns:
        List of SQL queries to execute the teardown
    """
    return [
        f"USE DATABASE {database};",
        f"DROP SCHEMA IF EXISTS {schema} CASCADE;"
    ]

def main() -> None:
    """Execute schema teardown for PR environments.
    
    Retrieves environment variables for PR number and database,
    connects to Snowflake, and drops the PR-specific schema.
    """
    pr_number = os.getenv('GITHUB_PR_NUMBER')
    database = os.getenv('SNOWFLAKE_PR_DATABASE')
    schema = f'github_pr_{pr_number}'

    print(f"\nConnecting to Snowflake...")
    conn = connect_to_snowflake()
    print("Successfully connected to Snowflake")
    
    print(f"\nDropping schema {schema} from database {database}...")
    queries = get_removal_queries(database, schema)
    execute_queries(conn, queries)
    
    print("\nTeardown completed")
    conn.close()
    print("Connection closed")


main()