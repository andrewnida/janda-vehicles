import psycopg2
from psycopg2 import sql
from urllib.parse import quote

def format_uri(input_string):
    return quote(input_string.strip().lower().replace(' ', '-'))

def connect_to_database_server(host, user, password, database=None):
    conn = None  # Define `conn` to ensure it's in scope

    try:
        # Establish connection
        print(f"Establishing a connection to {host}")
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        print(f"Connected to {host}")
        return conn

    except psycopg2.Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        # Cleanup only if `conn` was defined but failed to connect
        if conn and conn.closed:
            print("Connection will be closed due to unsuccessful connection")
    
    return None  # Explicitly return `None` if an error occurred

def create_database(conn, database, overwrite=False):
    try:
        # Use the existing connection
        conn.autocommit = True
        cursor = conn.cursor()

        # Query to check if the database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database,))
        result = cursor.fetchone()

        if result:
            if overwrite:
                # Drop the existing database
                print(f"Database '{database}' exists. Overwriting...")
                cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(database)))
                print(f"Database '{database}' has been dropped.")
            else:
                print(f"Database '{database}' exists. Overwrite not allowed.")
                
                return False

        # Create the new database
        print(f"Creating database '{database}'...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
        print(f"Database '{database}' created successfully.")
        
        return True
    except psycopg2.Error as e:
        print(f"Error while handling the database: {e}")
        return None
    finally:
        cursor.close()

def execute_query(conn, query):
    try:
        # Use a transaction with multiple statements
        cursor = conn.cursor()

        # Execute each statement in the transaction (or any query)
        for statement in filter(None, query.split(';')):
            if len(statement.strip()):
                cursor.execute(statement.strip() + ';')
        
        # Commit the transaction
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

# Helper for disconnecting from the DB
def disconnect_from_database_server(conn):
    if conn and not conn.closed:
        conn.close()
        print("Connection closed successfully")