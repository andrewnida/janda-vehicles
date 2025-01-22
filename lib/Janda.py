import os
# from src.database.database_utils import connect_to_database_server, create_database, disconnect_from_database_server

class Janda:
    def __init__(self):
        print(os.getenv('DEBUG'))
        # self.conn = connect_to_database_server(
        #     os.getenv('DB_HOST'), 
        #     os.getenv('DB_USER'), 
        #     os.getenv('DB_PASSWORD')
        # )

    # def select_database(self):
    #     if not self.conn:
    #         print(f"Failed to establish a connection to {os.getenv('DB_HOST')}")
    #         return

    #     while True:
    #         database = input("Database name: ").strip()
    #         if not database:
    #             print("Database name cannot be empty. Please try again.")
    #             continue

    #         res = create_database(self.conn, database)

    #         if res is None:
    #             print(f"Failed to create database: {database}")
    #             break  # Exit due to connection error
    #         elif res is False:
    #             # Database exists
    #             overwrite = input("Overwrite existing database? (y/n): ").strip().lower() == 'y'
    #             if overwrite:
    #                 create_database(self.conn, database, overwrite=True)
    #                 self.database = database
    #                 break  # Exit after overwriting
    #             else:
    #                 existing = input("Use existing database? (y/n): ").strip().lower() == 'y'
    #                 if existing:
    #                     self.database = database
    #                     break
    #                 else:
    #                     print("Database overwrite canceled. Please choose another name.")
    #                     continue  # Prompt again for a database name
    #         else:
    #             # Database successfully created
    #             self.database = database
    #             break

    #     # Print out the results of the database creation
    #     if self.database: 
    #         print(f"Selected database '{self.database}'")
    #     else: 
    #         print("No database selected")

    # def create_vehicle_tables(self):
    #     print('yay')

    # def dispose(self):
    #     if self.conn:
    #         disconnect_from_database_server(self.conn)
