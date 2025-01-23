from dotenv import load_dotenv
from database.DatabaseManager import DatabaseManager

# Check that script is being run directly
if __name__ == "__main__":
    # Load .env file
    load_dotenv()
    
    # Create application instance
    databaseManager = DatabaseManager()

    # Prompt the user for a database and create it if necessary
    databaseManager.select_database()

    # Try to create the tables for vehicles in the database
    databaseManager.create_vehicle_tables()

    # Disconnect from database and clean up
    databaseManager.dispose()
