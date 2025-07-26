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
import sqlite3, os, sys
import argparse

def generate_encounter(party_size, party_level, difficulty):
    threat_levels = {"trivial": 10,
                     "low": 15,
                     "moderate": 20,
                     "severe": 30,
                     "extreme": 40
	}
    xp_budget = party_size * threat_levels[difficulty]
    party_avg = party_level // party_size
    print(f"Party Level Average: {party_avg}")
    print(f"Total XP Budget: {xp_budget}")
    lower_monster_bound = party_avg - 4
    upper_monster_bound = party_avg + 4

    monsterConn = sqlite3.connect("creatures.db")
    monsterCurs = monsterConn.cursor()

    temp_table_creation = '''
            CREATE TEMP TABLE temp_table AS
			SELECT *
            FROM monsters 
			WHERE level BETWEEN ? AND ?
    '''
    output = []

    monsterCurs.execute(temp_table_creation, (lower_monster_bound, upper_monster_bound))

    while xp_budget > 0:
        
        monster = monsterCurs.execute('''
				SELECT name, level FROM temp_table ORDER BY RANDOM() LIMIT 1
		''')
        monsterVals = monster.fetchone()
        xp_ratio = party_avg - monsterVals[1]
		
        match xp_ratio:
                case 4:
                    if xp_budget >= 10:
                        xp_budget -= 10
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 10")
                case 3:
                    if xp_budget >= 15:
                        xp_budget -= 15
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 15")
                case 2:
                    if xp_budget >= 20:
                        xp_budget -= 20
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 20")
                case 1:
                    if xp_budget >= 30:
                        xp_budget -= 30
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 30")
                case 0:
                    if xp_budget >= 40:
                        xp_budget -= 40
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 40")
                case -1:
                    if xp_budget >= 60:
                        xp_budget -= 60
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 60")
                case -2:
                    if xp_budget >= 80:
                        xp_budget -= 80
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 80")
                case -3:
                    if xp_budget >= 120:
                        xp_budget -= 120
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 120")
                case -4:
                    if xp_budget >= 160:
                        xp_budget -= 160
                        output.append(f"Name: {monsterVals[0]}, Level: {monsterVals[1]}, XP: 160")

    print(output)
    monsterConn.close()
    return output

def main():

    def parse_arguments():
        parser = argparse.ArgumentParser(description="Pathfinder 2e Enemy Encounter Generator")
        parser.add_argument('--party-size', type=int, help="Size of the party (1-4)", required=True)
        parser.add_argument('--party-level', type=int, help="Level of the party (1-20)", required=True)
        parser.add_argument('--difficulty', type=str, choices=['trivial', 'low', 'moderate', 'severe', 'extreme'], 
                            help="Difficulty level of the encounter", required=True)
        args = parser.parse_args()

        # Validate party size
        if not (1 <= args.party_size <= 4):
            print("Error: Party size must be between 1 and 4.")
            sys.exit(1)

        # Validate party level
        if not (1 <= args.party_level <= 20):
            print("Error: Party level must be between 1 and 20.")
            sys.exit(1)

        return args

    running = True
    while running:
        print("\nWelcome to the Pathfinder 2e Enemy Encounter Generator!")
        args = parse_arguments()

        party_size = args.party_size
        party_level = args.party_level
        difficulty = args.difficulty

        
        print(f"Party Size: {party_size}, Party Level: {party_level}, Difficulty: {difficulty}")
        # TODO: Add logic to generate encounters based on the parsed arguments
        generate_encounter(party_size, party_level, difficulty)
            

        running = False  # Exit after one run for now

    print("Encounter generation complete. Thank you for using the Pathfinder 2e Enemy Encounter Generator!")
        
if __name__ == '__main__':
    main()

