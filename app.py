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

# def get_party_size():
#     while True:
#         try:
#             party_size = int(input("Enter party size (1-4): "))
#             if 1 <= party_size <= 4:
#                 return party_size
#             else:
#                 print("Party size must be between 1 and 4.")
#         except ValueError:
#             print("Invalid input. Please enter a numeric value.")

# def get_party_level():
#     while True:
#         try:
#             party_level = int(input("Enter party level (1-20): "))
#             if 1 <= party_level <= 20:
#                 return party_level
#             else:
#                 print("Party level must be between 1 and 20.")
#         except ValueError:
#             print("Invalid input. Please enter a valid numeric value.")


def main():

    def parse_arguments():
        parser = argparse.ArgumentParser(description="Pathfinder 2e Enemy Encounter Generator")
        parser.add_argument('--party-size', type=int, help="Size of the party (1-4)", required=True)
        parser.add_argument('--party-level', type=int, help="Level of the party (1-20)", required=True)
        parser.add_argument('--difficulty', type=str, choices=['easy', 'moderate', 'hard', 'severe'], 
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

        running = False  # Exit after one run for now

    print("Encounter generation complete. Thank you for using the Pathfinder 2e Enemy Encounter Generator!")
        
if __name__ == '__main__':
    main()

