import sqlite3, json, os, sys

with open('beastiary/monsters.json', 'r') as monster_json:
    monster_data = json.load(monster_json)

conn = sqlite3.connect('creatures.db')  # Connect to the SQLite database
cursor = conn.cursor()  # Create a cursor to execute SQL commands

with open('table_schema.sql', 'r') as schema_file:
    schema = schema_file.read()
    cursor.executescript(schema)  # Execute the SQL script to create the table

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
print("Database 'monsters.db' created and populated with monster data.")


