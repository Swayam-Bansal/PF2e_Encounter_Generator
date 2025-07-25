"""
Pathfinder 2e Enemy Encounter Generator App

Summary:
This CLI-based app helps Game Masters quickly generate balanced enemy encounters for Pathfinder 2e. 
Users input party size, party level, and terrain type. 
The backend uses a simple monster dataset (JSON) containing monster name, challenge rating (CR), terrain, HP, and abilities. 
The app selects appropriate enemies based on party level and terrain, then outputs a list of enemies with their stats.

Features:
- User Inputs: Party size, party level, terrain type
- Backend: Monster dataset, encounter logic matching CR and terrain
- Frontend: CLI input prompts, output of enemy list with stats
- Bonus: Regenerate encounters, save/load encounter data
"""

# Import necessary libraries
# import sqlite3, requests, json, os, sys
import sqlite3, json, os, sys

# Create a simple SQLite database to store monster data
def create_database():
    monster_json_path = 'beastiary/monsters.json'
    if not os.path.exists(monster_json_path):
        print("Monster data file not found. Please ensure 'monsters.json' exists in the current directory.")
        sys.exit(1)
    with open(monster_json_path, 'r') as monster_json:
        monster_data = json.load(monster_json)

    db_monster = 'monsters.db'
    db_connection = sqlite3.connect(db_monster) # Connect to the SQLite database
    db_cursor = db_connection.cursor() # Create a cursor to execute SQL commands

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
                VALUES (?, ?, ?)''',
                (name, level, traits, description))
        except sqlite3.Error as e:
            print(f"Error inserting {name}: {e}")

    db_connection.commit() # Commit the changes to the database
    db_connection.close() # Close the database connection
    print(f"Database '{db_monster}' created and populated with monster data.")

if __name__ == '__main__':
    create_database()
