'''
This app is intended to be used with the PF2e Encounter Generator to convert 
from CLI to a CDUD web application.
'''

# Imports
from flask import Flask, jsonify, render_template
import sqlite3

# Initialize Flask application
app = Flask(__name__)

# Link the SQLite database generated
app.config["DATABASE"] = "creatures.db"

# Function to fetch all monster data from the database we previously created
# with the CLI tool. In the future, the CLI tool will either be integrated
# into this app or the app will be able to call the CLI tool to update the database

def get_all_monsters():
    try:
        connection = sqlite3.connect(app.config["DATABASE"])
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, level FROM sorted_table")
        results = cursor.fetchall()
        print("DEBUG: Monsters fetched from DB:", results)
        return results
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return []
    finally:
        connection.close()

# Route to serve the index page
@app.route("/")
def index():
    monsters = get_all_monsters()
    return render_template("index.html", monsters=monsters)

if __name__ == "__main__":
    app.run(debug=True) # This will run the Flask web app in debug mode
