import sqlite3, json, glob, os
import constants

def create_tables():
    conn = sqlite3.connect(constants.DB_NAME)  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands

    with open('table_schema.sql', 'r') as schema_file:
        schema = schema_file.read()
        cursor.executescript(schema)  # Execute the SQL script to create the table

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection 


def import_all_data():
    json_paths = glob.glob(os.path.join(constants.CREATURES_JSON_PATH, '*.json'))  # Get all JSON files in the specified directory

    conn = sqlite3.connect(constants.DB_NAME)  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands

    for path in json_paths:
        with open(path, 'r') as monster_json:
            monster_data = json.load(monster_json)

        # with open('beastiary/creatures-afof.json', 'r') as monster_json:  # Load the JSON data from the file
        #     monster_data = json.load(monster_json)
        
        # Insert each monster into the database
        for monster in monster_data['creature']:
            name = monster.get('name', 'Unknown')  # Get monster name, default to 'Unknown'
            level = monster.get('level', 0)  # Get monster level, default to 0
            description = monster.get('description', 'No description available')  # Get monster description

            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO monsters (name, level, description)
                    VALUES (?, ?, ?)''',
                    (name, level, description))
            except sqlite3.Error as e:
                print(f"Error inserting {name}: {e}")

        conn.commit()  # Commit the changes to the database

    conn.close()  # Close the database connection
    print("Database created and populated with monster data.")


