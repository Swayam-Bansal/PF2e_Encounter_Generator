import os, sys
import db_loader, constants

if __name__ == "__main__":
    args = sys.argv[1:]

    if "setup" in args:
        print("Initializing the Pathfinder 2e Encounter Generator setup...")
        
        # Scraping JSON files from GitHub
        print("Scraping JSON files all the creatures...")
        print("JSON files scraped and downloaded successfully.")
        
        # Setting up the database
        print("Setting up the database...")
        if os.path.exists(constants.DB_NAME):
            os.remove(constants.DB_NAME)

        db_loader.create_tables()
        db_loader.import_all_data()
        print("DB setup complete.")

    
