import os

from psycopg2 import DatabaseError
from database.utils import connect_to_database_server, create_database, disconnect_from_database_server, execute_query, format_uri

# Acts as a layer between the Scrapy spider and the database
# Connects to the database on instantiation using env vars 
class DatabaseManager:
    def __init__(self):
        self.conn = connect_to_database_server(
            os.getenv('PG_HOST'), 
            os.getenv('PG_USER'),
            os.getenv('PG_PASSWORD'), 
            os.getenv('PG_DEFAULT_DB')
        )

    # This is useful just for convenience for the spider to use
    # This mainly just keeps this boilerplate code out of the sql templates
    def set_database(self, database):
        self.conn = connect_to_database_server(
            os.getenv('PG_HOST'), 
            os.getenv('PG_USER'),
            os.getenv('PG_PASSWORD'), 
            database
        )

        self.database = database

    # Prompt the user in the main setup script to get a database setup
    # Provides ability to overwrite an existing database, and confirms before overwriting
    def select_database(self):
        # No current connection
        if not self.conn:
            print(f"Failed to establish a connection to {os.getenv('PG_HOST')}")
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

    # Pass a pipeline item to be inserted into the DB
    def insert_vehicle(self, vehicle):
        # Format all the display names for URI using the helper function
        vehicle["region_uri"] = format_uri(vehicle["region_display"])
        vehicle["make_uri"] = format_uri(vehicle["make_display"])
        vehicle["model_uri"] = format_uri(vehicle["model_display"])
        vehicle["trim_uri"] = format_uri(vehicle["trim_display"])

        if "frame_display" in vehicle:
            self.insert_jdm_vehicle(vehicle)
        else:
            self.insert_usdm_vehicle(vehicle)

        print(f"Vehicle {vehicle["make_display"]} {vehicle["model_display"]} {vehicle["trim_display"]} added to database {self.database}")

    def insert_jdm_vehicle(self, vehicle):
        vehicle["frame_uri"] = format_uri(vehicle["frame_display"])
        vehicle["chasiss_uri"] = format_uri(vehicle["chasiss_display"])

        try:
            self.conn.autocommit = False
            cursor = self.conn.cursor()

            # Region
            cursor.execute(
                """
                SELECT id FROM regions WHERE uri = %s
                """,
                (vehicle["region_uri"],)
            )

            result = cursor.fetchone()

            if result:
                region_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO regions (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["region_uri"], vehicle["region_display"])
                )
                region_id = cursor.fetchone()[0]

            # Make
            cursor.execute(
                """
                SELECT id FROM makes WHERE uri = %s
                """,
                (vehicle["make_uri"],)
            )

            result = cursor.fetchone()

            if result:
                make_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO makes (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["make_uri"], vehicle["make_display"])
                )
                make_id = cursor.fetchone()[0]

            # Model
            cursor.execute(
                """
                SELECT id FROM models WHERE uri = %s
                """,
                (vehicle["model_uri"],)
            )

            result = cursor.fetchone()

            if result:
                model_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO models (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["model_uri"], vehicle["model_display"])
                )
                model_id = cursor.fetchone()[0]

            # Frame
            cursor.execute(
                """
                SELECT id FROM frames WHERE uri = %s
                """,
                (vehicle["frame_uri"],)
            )

            result = cursor.fetchone()

            if result:
                frame_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO frames (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["frame_uri"], vehicle["frame_display"])
                )
                frame_id = cursor.fetchone()[0]

            # Chasiss
            cursor.execute(
                """
                SELECT id FROM chasiss WHERE uri = %s
                """,
                (vehicle["chasiss_uri"],)
            )

            result = cursor.fetchone()

            if result:
                chasiss_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO chasiss (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["chasiss_uri"], vehicle["chasiss_display"])
                )
                chasiss_id = cursor.fetchone()[0]

            # Frames chasiss
            cursor.execute(
                """
                SELECT id FROM frames_chasiss WHERE frame_id = %s AND chasiss_id = %s
                """,
                (frame_id, chasiss_id)
            )

            result = cursor.fetchone()

            if result:
                frames_chasiss_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO frames_chasiss (frame_id, chasiss_id)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (frame_id, chasiss_id)
                )
                frames_chasiss_id = cursor.fetchone()[0]

            # Frame numbers
            cursor.execute(
                """
                SELECT id FROM frame_nums WHERE num_from = %s AND num_to = %s
                """,
                (vehicle["frame_num_from"], vehicle["frame_num_to"])
            )

            result = cursor.fetchone()

            if result:
                frame_nums_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO frame_nums (num_from, num_to)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["frame_num_from"], vehicle["frame_num_to"])
                )
                frame_nums_id = cursor.fetchone()[0]

            # Frames Chasiss Frame Numbers
            cursor.execute(
                """
                SELECT id FROM frames_chasiss_frame_nums WHERE frames_chasiss_id = %s AND frame_nums_id = %s
                """,
                (frames_chasiss_id, frame_nums_id)
            )

            result = cursor.fetchone()

            if result:
                frames_chasiss_frame_nums_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO frames_chasiss_frame_nums (frames_chasiss_id, frame_nums_id)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (frames_chasiss_id, frame_nums_id)
                )
                frames_chasiss_frame_nums_id = cursor.fetchone()[0]

            # Body style
            if vehicle["doors"] == "2":
                body = "coupe"
            elif vehicle["doors"] == "3":
                body = "hatch"
            elif vehicle["doors"] == "4":
                body = "sedan"
            else:
                body = "van"

            cursor.execute(
                """
                SELECT id FROM body_styles WHERE body = %s AND doors = %s
                """,
                (body, vehicle["doors"])
            )

            result = cursor.fetchone()

            if result:
                body_style_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO body_styles (body, doors)
                    VALUES (%s, %s)
                    RETURNING id
                    """, 
                    (body, vehicle["doors"])
                ) 
                
                body_style_id = cursor.fetchone()[0]

            # Transmission
            cursor.execute(
                """
                SELECT id FROM transmissions WHERE code = %s AND speeds = %s
                """,
                (vehicle["transmission_code"], str(vehicle["transmission_speeds"]))
            )

            result = cursor.fetchone()

            if result:
                transmission_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO transmissions (code, speeds, auto)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (vehicle["transmission_code"], str(vehicle["transmission_speeds"]), vehicle["transmission_auto"])
                )
                transmission_id = cursor.fetchone()[0] 

            # Trim
            cursor.execute(
                """
                SELECT id FROM trims WHERE uri = %s
                """,
                (vehicle["trim_uri"],)
            )

            result = cursor.fetchone()

            if result:
                trim_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO trims (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["trim_uri"], vehicle["trim_display"])
                )
                trim_id = cursor.fetchone()[0] 

            # Vehicle
            cursor.execute(
                """
                SELECT id FROM vehicles WHERE scrape_path = %s
                """,
                (vehicle["vehicle_path"],)
            )

            result = cursor.fetchone()

            if result:
                vehicle_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO vehicles (region_id, make_id, model_id, frames_chasiss_frame_nums_id, body_style_id, transmission_id, trim_id, scrape_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (region_id, make_id, model_id, frames_chasiss_frame_nums_id, body_style_id, transmission_id, trim_id, vehicle["vehicle_path"])
                )
                vehicle_id = cursor.fetchone()[0]

            for option in vehicle["options"]:
                vehicle["option_display"] = option.title()
                vehicle["option_uri"] = format_uri(option)
                cursor.execute(
                    """
                    SELECT id FROM options WHERE uri = %s
                    """,
                    (vehicle["option_uri"],)
                )

                result = cursor.fetchone()

                if result:
                    option_id = result[0]
                else:
                    cursor.execute(
                        """
                        INSERT INTO options (uri, display)
                        VALUES (%s, %s)
                        RETURNING id
                        """,
                        (vehicle["option_uri"], vehicle["option_display"])
                    )
                    option_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO vehicle_options (vehicle_id, option_id)
                    VALUES (%s, %s)
                    """,
                    (vehicle_id, option_id)
                )
                
            self.conn.commit()
        except (Exception, DatabaseError) as error:
            print(f"Error: {error}")
            if self.conn:
                self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if self.conn:
                self.conn.close()

    def insert_usdm_vehicle(self, vehicle):
        vehicle["variant_uri"] = format_uri(vehicle["variant_display"])
        vehicle["area_code_uri"] = format_uri(vehicle["area_code_display"])

        try:
            self.conn.autocommit = False
            cursor = self.conn.cursor()

            # Region
            cursor.execute(
                """
                SELECT id FROM regions WHERE uri = %s
                """,
                (vehicle["region_uri"],)
            )

            result = cursor.fetchone()

            if result:
                region_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO regions (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["region_uri"], vehicle["region_display"])
                )
                region_id = cursor.fetchone()[0]

            # Make
            cursor.execute(
                """
                SELECT id FROM makes WHERE uri = %s
                """,
                (vehicle["make_uri"],)
            )

            result = cursor.fetchone()

            if result:
                make_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO makes (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["make_uri"], vehicle["make_display"])
                )
                make_id = cursor.fetchone()[0]

            # Model
            cursor.execute(
                """
                SELECT id FROM models WHERE uri = %s
                """,
                (vehicle["model_uri"],)
            )

            result = cursor.fetchone()

            if result:
                model_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO models (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["model_uri"], vehicle["model_display"])
                )
                model_id = cursor.fetchone()[0]

            # Body style
            if vehicle["doors"] == "2":
                body = "coupe"
            elif vehicle["doors"] == "3":
                body = "hatch"
            elif vehicle["doors"] == "4":
                body = "sedan"
            else:
                body = "van"

            cursor.execute(
                """
                SELECT id FROM body_styles WHERE body = %s AND doors = %s
                """,
                (body, vehicle["doors"])
            )

            result = cursor.fetchone()

            if result:
                body_style_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO body_styles (body, doors)
                    VALUES (%s, %s)
                    RETURNING id
                    """, 
                    (body, vehicle["doors"])
                ) 
                
                body_style_id = cursor.fetchone()[0]

            # Transmission
            cursor.execute(
                """
                SELECT id FROM transmissions WHERE code = %s AND speeds = %s
                """,
                (vehicle["transmission_code"], str(vehicle["transmission_speeds"]))
            )

            result = cursor.fetchone()

            if result:
                transmission_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO transmissions (code, speeds, auto)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (vehicle["transmission_code"], str(vehicle["transmission_speeds"]), vehicle["transmission_auto"])
                )
                transmission_id = cursor.fetchone()[0] 

            # Trim
            cursor.execute(
                """
                SELECT id FROM trims WHERE uri = %s
                """,
                (vehicle["trim_uri"],)
            )

            result = cursor.fetchone()

            if result:
                trim_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO trims (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["trim_uri"], vehicle["trim_display"])
                )
                trim_id = cursor.fetchone()[0]

            # Variant
            cursor.execute(
                """
                SELECT id FROM variants WHERE uri = %s
                """,
                (vehicle["variant_uri"],)
            )

            result = cursor.fetchone()

            if result:
                variant_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO variants (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["variant_uri"], vehicle["variant_display"])
                )
                variant_id = cursor.fetchone()[0] 

            # Area Code
            cursor.execute(
                """
                SELECT id FROM area_codes WHERE uri = %s
                """,
                (vehicle["area_code_uri"],)
            )

            result = cursor.fetchone()

            if result:
                area_code_id = result[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO area_codes (uri, display)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (vehicle["area_code_uri"], vehicle["area_code_display"])
                )
                area_code_id = cursor.fetchone()[0] 

            # Vehicle
            cursor.execute(
                """
                SELECT id FROM vehicles WHERE scrape_path = %s
                """,
                (vehicle["vehicle_path"],)
            )

            result = cursor.fetchone()

            if not result:
                cursor.execute(
                    """
                    INSERT INTO vehicles (region_id, make_id, model_id, year, body_style_id, transmission_id, trim_id, variant_id, area_code_id, scrape_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (region_id, make_id, model_id, vehicle["year"], body_style_id, transmission_id, trim_id, variant_id, area_code_id, vehicle["vehicle_path"])
                )
                
            self.conn.commit()
        except (Exception, DatabaseError) as error:
            print(f"Error: {error}")
            if self.conn:
                self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if self.conn:
                self.conn.close()

    # Initial setup function that calls the sql script to make all the tables
    def create_vehicle_tables(self):
        if self.conn.closed:
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
