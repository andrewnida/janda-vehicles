import mysql.connector
from urllib.parse import quote

def format_uri(input_string):
    return quote(input_string.strip().lower().replace(' ', '-'))

def connect_to_database_server(host, user, password, database=None):
    conn = None  # Define `conn` to ensure it's in scope

    try:
        # Establish connection
        print(f"Establishing a connection to {host}")
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Check if connection is successful
        if conn.is_connected():
            print(f"Connected to {conn.server_host}:{conn.server_port}")
            
            return conn
        else:
            raise Exception("Connection failed: Unable to connect to the database")

    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        # Cleanup only if `conn` was defined but not connected
        if conn and not conn.is_connected():
            print("Connection will be closed due to unsuccessful connection")
    
    return None  # Explicitly return `None` if an error occurred

def create_database(conn, database, overwrite=False):
    try:
        # Use the existing connection
        cursor = conn.cursor()

        # Query to check if the database exists
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database}'")
        result = cursor.fetchone()

        if result:
            if overwrite:
                # Drop the existing database
                print(f"Database '{database}' exists. Overwriting...")
                cursor.execute(f"DROP DATABASE `{database}`")
                print(f"Database '{database}' has been dropped.")
            else:
                print(f"Database '{database}' exists. Overwrite not allowed.")
                
                return False

        # Create the new database
        print(f"Creating database '{database}'...")
        cursor.execute(f"CREATE DATABASE `{database}`")
        print(f"Database '{database}' created successfully.")
        
        return True
    except mysql.connector.Error as e:
        print(f"Error while handling the database: {e}")
        
        return None
    finally:
        cursor.close()  # Close the cursor, but keep the connection open for reuse

def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        conn.autocommit = False

        for i in filter(None, query.split(';')):
            cursor.execute(i.strip() + ';')
        
        conn.commit()
        
        return True
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        
        return False
    finally:
        cursor.close()

def disconnect_from_database_server(conn):
    conn.cursor().close()
    conn.close()
    print("Connection closed successfully")