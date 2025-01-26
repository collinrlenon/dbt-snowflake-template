import os
import snowflake.connector

def connect_to_snowflake():
    """Establish connection to Snowflake using environment variables."""
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_ADMIN_USER'),
        password=os.getenv('SNOWFLAKE_ADMIN_PASSWORD'),
    )

def execute_queries(conn, queries):
    """Execute a list of queries in sequence."""
    cur = conn.cursor()
    for query in queries:
        try:
            cur.execute(query)
            print(f"Successfully executed: {query}")
        except Exception as e:
            print(f"Error executing query: {query}")
            print(f"Error message: {str(e)}")

    cur.close() 