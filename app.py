"""
Pathfinder 2e Enemy Encounter Generator App

Summary:
This CLI-based app helps Game Masters quickly generate balanced enemy encounters for Pathfinder 2e. 
Users input party size, party level, and terrain type. 
The backend uses a simple monster dataset (JSON) containing monster name, challenge rating (CR), terrain, HP, and abilities. 
The app selects appropriate enemies based on party level and terrain, then outputs a list of enemies with their stats.

Features:
- User Inputs: Party size, party level
- Backend: Monster dataset, encounter logic matching CR and terrain
- Frontend: CLI input prompts, output of enemy list with stats
- Bonus: Regenerate encounters, save/load encounter data
"""

# Import necessary libraries
# import sqlite3, requests, json, os, sys
import sqlite3, json, os, sys
# import constants

# Create a simple SQLite database to store monster data
def create_database():
    monster_json_path = 'beastiary/monsters.json'
    if not os.path.exists(monster_json_path):
        print("Monster data file not found. Please ensure 'beastiary/monsters.json' exists")
        sys.exit(1)
    with open(monster_json_path, 'r') as monster_json:
        monster_data = json.load(monster_json)

    db_monster = 'monsters.db'
    db_connection = sqlite3.connect(db_monster) # Connect to the SQLite database
    db_cursor = db_connection.cursor() # Create a cursor to execute SQL commands

    create_table(db_monster) # Generate monster table on first execution

    # Create monsters table if it doesn't exist
    for monster in monster_data:
        name = monster.get('name', 'Unknown') # Get monster name, default to 'Unknown'
        level = monster.get('level', 0) # Get monster level, default to 0
        traits = monster.get('traits', []) # Get monster traits, default to empty list
        description = monster.get('description', 'No description available') # Get monster description
        # TODO: Add more fields as necessary

        try:
            db_cursor.execute('''
                INSERT OR REPLACE INTO monsters (name, level, traits, description)
                VALUES (?, ?, ?, ?)''',
                (name, level, traits, description))
        except sqlite3.Error as e:
            print(f"Error inserting {name}: {e}")

    db_connection.commit() # Commit the changes to the database
    db_connection.close() # Close the database connection
    print(f"Database '{db_monster}' created and populated with monster data.")

def create_table(DB_NAME):
    if os.path.exists(DB_NAME):
        print(f"Database '{DB_NAME}' already exists.")

    conn = sqlite3.connect(DB_NAME) # Connect to the database
    cursor = conn.cursor() # Create a cursor to execute SQL commands

    #Create monsters table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monsters (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        level INTEGER NOT NULL,
                        traits TEXT NOT NULL,
                        description TEXT NOT NULL
                    )''') # Create monsters table with columns: id, name, level, traits, description
    conn.commit() 
    conn.close() 

def get_party_size():
    while True:
        try:
            party_size = int(input("Enter party size (1-4): "))
            if 1 <= party_size <= 4:
                return party_size
            else:
                print("Party size must be between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_party_level():
    while True:
        try:
            party_level = int(input("Enter party level (1-20): "))
            if 1 <= party_level <= 20:
                return party_level
            else:
                print("Party level must be between 1 and 20.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")


def main():
    if not os.path.exists('monsters.db'):
        print("Database not found, creating...")
        create_database()
        create_table('monsters.db') # Create the monsters table
        print("Database 'monsters.db' created successfully.")
    else:
        print("Using existing database 'monsters.db'")

    conn = sqlite3.connect('monsters.db') # Connect to the SQLite database

    running = True

    while running:
        print("\nWelcome to the Pathfinder 2e Enemy Encounter Generator!")
        get_party_size()
        get_party_level()
        terrain = input("Enter terrain type (e.g., forest, dungeon): ")
        flag = False

        try:
            party_size = int(party_size)
            party_level = int(party_level)
            if party_size <= 0 and party_level <= 0:
                print("Party size and level must be positive integers.")
                continue
        except ValueError:
            print("Invalid input. Please enter numeric values for party size and level.")
            continue
        
if __name__ == '__main__':
    main()

