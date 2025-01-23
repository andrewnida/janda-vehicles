import os
from database.utils import connect_to_database_server, create_database, disconnect_from_database_server, execute_query

class DatabaseManager:
    def __init__(self):
        self.conn = connect_to_database_server(
            os.getenv('DB_HOST'), 
            os.getenv('DB_USER'), 
            os.getenv('DB_PASSWORD')
        )

    def select_database(self):
        if not self.conn:
            print(f"Failed to establish a connection to {os.getenv('DB_HOST')}")
            return

        while True:
            database = input("Database name: ").strip()
            if not database:
                print("Database name cannot be empty. Please try again.")
                continue

            res = create_database(self.conn, database)

            if res is None:
                print(f"Failed to create database: {database}")
                break  # Exit due to connection error
            elif res is False:
                # Database exists
                overwrite = input("Overwrite existing database? (y/n): ").strip().lower() == 'y'
                if overwrite:
                    create_database(self.conn, database, overwrite=True)
                    self.database = database
                    break  # Exit after overwriting
                else:
                    existing = input("Use existing database? (y/n): ").strip().lower() == 'y'
                    if existing:
                        self.database = database
                        break
                    else:
                        print("Database overwrite canceled. Please choose another name.")
                        continue  # Prompt again for a database name
            else:
                # Database successfully created
                self.database = database
                break

        # Print out the results of the database creation
        if self.database: 
            execute_query(self.conn, f"USE {self.database}")
            print(f"Selected database '{self.database}'")
        else: 
            print("No database selected")

    def create_vehicle_tables(self):
        if not self.conn.is_connected():
            print("No connection...skipping creating vehicle tables")
            return
        elif not self.database:
            print("No database...skipping creating vehicle tables")
            return
        
        with open("./database/queries/make_vehicles.sql", 'r') as file:
            query = file.read()

        if execute_query(self.conn, query):
            print("Vehicle tables created succesfully")
        else:
            print("Vehicle tables were unable to be created")

    def dispose(self):
        if self.conn:
            disconnect_from_database_server(self.conn)
