'''
This app is intended to be used with the PF2e Encounter Generator to convert 
from CLI to a CDUD web application.
'''

# Imports
from flask import Flask, jsonify, render_template, request
import sqlite3

# Initialize Flask application
app = Flask(__name__)

# Link the SQLite database generated
app.config["DATABASE"] = "creatures.db"

# Function to fetch all monster data from the database we previously created
# with the CLI tool. In the future, the CLI tool will either be integrated
# into this app or the app will be able to call the CLI tool to update the database

def generate_encounter(party_size, party_level, difficulty):
    threat_levels = {"trivial": 10, "low": 15, "moderate": 20, "severe": 30, "extreme": 40}
    xp_budget = party_size * threat_levels[difficulty]
    # party_level = party_level // party_size
    output = []

    if party_level > 21:
        raise ValueError("Party average level too high.")
    if party_level == 1 and threat_levels[difficulty] < 20:
        xp_budget = 20
    elif party_level == 2 and threat_levels[difficulty] < 15:
        xp_budget = 15

    # Define lower and upper bounds for monster level selection
    lower = max(party_level - 4, -1)  # prevent access to monster level of lower then -1
    upper = party_level + 4

    conn = sqlite3.connect(app.config["DATABASE"])
    cursor = conn.cursor()

    # Create or replace valid_table as a filter of monsters by level range
    cursor.execute("DROP TABLE IF EXISTS valid_table")
    cursor.execute('''
        CREATE TABLE valid_table AS
        SELECT * FROM monsters WHERE level BETWEEN ? AND ?
    ''', (lower, upper))

    # Generate encounter by randomly selecting monsters from valid_table
    while xp_budget >= 10:
        monster = cursor.execute('''
            SELECT name, level FROM valid_table ORDER BY RANDOM() LIMIT 1
        ''').fetchone()
        if not monster:
            break

        name, level = monster
        xp_ratio = party_level - level

        # Mapping XP costs based on the difference between party average and monster level
        cost_lookup = {
            4: 10, 3: 15, 2: 20, 1: 30, 0: 40,
            -1: 60, -2: 80, -3: 120, -4: 160
        }

        xp_cost = cost_lookup.get(xp_ratio)
        if xp_budget >= xp_cost:
            xp_budget -= xp_cost
            output.append((name, level, xp_cost))
        else:
            # If no suitable monster fits XP budget, try again
            continue

    conn.commit()
    conn.close()
    return output

# Save the generated encounter to a new table called encounter_table
def save_encounter_to_db(encounter):
    conn = sqlite3.connect(app.config["DATABASE"])
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS encounter_table")
    cursor.execute('''
        CREATE TABLE encounter_table (
            name TEXT,
            level INTEGER,
            xp_cost INTEGER
        )
    ''')
    cursor.executemany('''
        INSERT INTO encounter_table (name, level, xp_cost) VALUES (?, ?, ?)
    ''', encounter)

    conn.commit()
    conn.close()

# Fetch all monsters from encounter_table for display
def get_encounter_monsters():
    try:
        connection = sqlite3.connect(app.config["DATABASE"])
        connection.row_factory = sqlite3.Row  # Return rows as dict-like objects
        cursor = connection.cursor()
        cursor.execute("SELECT name, level, xp_cost FROM encounter_table")
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return []
    finally:
        connection.close()

# Route to serve the index page and handle form POST
@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    party_size = None
    party_level = None
    difficulty = None
    encounter = []
    monsters = []

    if request.method == "POST":
        try:
            party_size = int(request.form["party_size"])
            party_level = int(request.form["party_level"])
            difficulty = request.form["difficulty"]

            if not (1 <= party_size <= 8):
                raise ValueError("Party size must be between 1 and 8.")
            if not (1 <= party_level <= 160):
                raise ValueError("Party level must be between 1 and 160.")
            if difficulty not in ["trivial", "low", "moderate", "severe", "extreme"]:
                raise ValueError("Invalid difficulty.")

            # Generate the encounter using the input parameters
            encounter = generate_encounter(party_size, party_level, difficulty)

            # Save generated encounter to the database table
            save_encounter_to_db(encounter)

            # Retrieve monsters from the newly created encounter_table for display
            monsters = get_encounter_monsters()

        except ValueError as ve:
            error = "Value Error: " + str(ve)
        except Exception as e:
            error = "Something went wrong: " + str(e)

    # Render the index page with all data needed for the template
    return render_template(
        "index.html",
        encounter=encounter,
        monsters=monsters,
        party_size=party_size,
        party_level=party_level,
        difficulty=difficulty,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)  # This will run the Flask web app in debug mode
