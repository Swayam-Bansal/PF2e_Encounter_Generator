'''
This app is intended to be used with the PF2e Encounter Generator to convert 
from CLI to a CDUD web application.
'''

# Imports
from flask import Flask, jsonify, render_template, request
import sqlite3
from app import generate_encounter

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
        connection.row_factory = sqlite3.Row  # Ensure rows are returned as dictionaries for easier debugging
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, level FROM sorted_table")
        results = cursor.fetchall()  # Fetch all rows from the query
        print("DEBUG: Monsters fetched from DB:", [dict(row) for row in results])
        print("DEBUG: Monsters fetched from DB:", results)
        return results
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return []
    finally:
        connection.close()

# Route to serve the index page
@app.route("/", methods=["GET", "POST"])
def index():
    monsters = get_all_monsters()
    
    if request.method == "POST":
        try:
            # Parse form inputs
            party_size = int(request.form["party_size"])
            party_level = int(request.form["party_level"])
            difficulty = request.form["difficulty"]

            # Validate input ranges
            if not (1 <= party_size <= 8):
                raise ValueError("Party size must be between 1 and 8.")

            if not (1 <= party_level <= 160):
                raise ValueError("Party level must be between 1 and 160.")

            if difficulty not in ["trivial", "low", "moderate", "severe", "extreme"]:
                raise ValueError("Invalid difficulty selection.")

            # Generate encounter
            output = generate_encounter(party_size, party_level, difficulty)
            return render_template("index.html", encounter=output)

        except ValueError as ve:
            return render_template("index.html", error="Value Error: " + str(ve))

        except Exception as e:
            return render_template("index.html", error="Something went wrong: " + str(e))


    else:
        return render_template("index.html", monsters=monsters)

if __name__ == "__main__":
    app.run(debug=True) # This will run the Flask web app in debug mode
