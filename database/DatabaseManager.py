import os
from database.utils import connect_to_database_server, create_database, disconnect_from_database_server, execute_query, format_uri

# Acts as a layer between the Scrapy spider and the database
# Connects to the database on instantiation using env vars 
class DatabaseManager:
    def __init__(self):
        self.conn = connect_to_database_server(
            os.getenv('DB_HOST'), 
            os.getenv('DB_USER'), 
            os.getenv('DB_PASSWORD')
        )

    # This is useful just for convenience for the spider to use
    # This mainly just keeps this boilerplate code out of the sql templates
    def set_database(self, database):
        self.database = database
        execute_query(self.conn, f"USE {self.database}")
        print(f"Selected database '{self.database}'")

    # Pass a pipeline item to be inserted into the DB
    def insert_vehicle(self, vehicle):
        # Format all the display names for URI using the helper function
        vehicle["region_uri"] = format_uri(vehicle["region_display"])
        vehicle["make_uri"] = format_uri(vehicle["make_display"])
        vehicle["model_uri"] = format_uri(vehicle["model_display"])
        vehicle["trim_uri"] = format_uri(vehicle["trim_display"])

         # Infer coming from JDM market if frame present
         # Then do some more URI formatting
        if "frame_display" in vehicle:
            vehicle["frame_uri"] = format_uri(vehicle["frame_display"])
            vehicle["chasiss_uri"] = format_uri(vehicle["chasiss_display"])
            query_path = './database/queries/insert_jdm_vehicle.sql'
        else:
            vehicle["variant_uri"] = format_uri(vehicle["variant_display"])
            vehicle["area_code_uri"] = format_uri(vehicle["area_code_display"])
            query_path = './database/queries/insert_usdm_vehicle.sql'

        # Open up the correct query path for its market
        # Inject the pipeline item into the query
        # Use the convenience function to execute the query on the open connection
        with open(query_path, 'r') as file:
            query_template = file.read()
        query = query_template.format(**vehicle)
        execute_query(self.conn, query)

        # Open up the options sql template
        with open('./database/queries/insert_vehicle_option.sql', 'r') as file:
            query_template = file.read()

        # Loop through each option and temporarily store it just so the template can inject it
        # Then call the execution of the statement for each option
        for option in vehicle["options"]:
            vehicle["option_display"] = option.title()
            vehicle["option_uri"] = format_uri(option)
            query = query_template.format(**vehicle)
            execute_query(self.conn, query)

        print(f"Vehicle {vehicle["make_display"]} {vehicle["model_display"]} {vehicle["trim_display"]} added to database {self.database}")

    # Prompt the user in the main setup script to get a database setup
    # Provides ability to overwrite an existing database, and confirms before overwriting
    def select_database(self):
        # No current connection
        if not self.conn:
            print(f"Failed to establish a connection to {os.getenv('DB_HOST')}")
            return

        # Main program loop and keep executing til we break out and have a database name
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
                    self.set_database(database) 
                    break  # Exit after overwriting
                else:
                    existing = input("Use existing database? (y/n): ").strip().lower() == 'y'
                    if existing:
                        self.set_database(database) 
                        break
                    else:
                        print("Database overwrite canceled. Please choose another name.")
                        continue  # Prompt again for a database name
            else:
                # Database successfully created
                self.set_database(database)
                break

        # Print out the results of the database creation
        if not self.database:
            print("No database selected")

    # Initial setup function that calls the sql script to make all the tables
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

    # Convenience method to clean up the DB connection when finishing
    def dispose(self):
        if self.conn:
            disconnect_from_database_server(self.conn)
