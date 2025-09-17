import json
import os
import random
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()

# Retrieve values from .env.
tbaEventKey: str = os.getenv("TBA_EVENT_KEY")   # From FIRST/The Blue Alliance

# Define the status function.
def status(message):
    print(f"{datetime.now()}: {message}")

# Validate argument.
if tbaEventKey == "":
    status("No event key provided.")
    exit()    


team_members = [
    "Abyss Mortimer",
    "Alex Phillips",
    "Amanah Obaji",
    "Andrew McCadden",
    "Ariana Toner",
    "Asher Stuckey",
    "Autumn Schoenfeld",
    "Brandon Bates",
    "Carter Silva",
    "Celton Norter",
    "Colby Jackson",
    "Colden Stubbe",
    "Connor Toper",
    "Dean Blanchard",
    "Domenic Giammusso",
    "Greydon Jones-Dulisse",
    "Hamza Keles",
    "Jackson Newcomb",
    "Jacob LeBlanc",
    "Jacob Wyrozebski",
    "Jesse White",
    "Jonah Woika",
    "Jonathan Brouillard",
    "Jordan Fenton",
    "Kai Hurrell",
    "Kai Wilbur",
    "Lukas Harrison",
    "Maddie DeCicca",
    "Mason Silva",
    "Matthew Mazzota",
    "Nanson Chen",
    "Nicholas Munier",
    "Ruthie Christensen",
    "Sam Clark",
    "Shawn Estrich",
    "Siena Reeve",
    "Simon Stuckey",
    "TJ Blake",
    "Tyler Hignett",
]


# Define a function that accepts the match number, the alliance, and the team keys.
# This function will fabricate scouting data for each team in the alliance.
def create_record_for_team(match, alliance, keys):
    # Set up weights.
    weights_bool = [0.1, 0.9]
    auto_coral_weights = [0.1, 0.8, 0.1]
    tele_coral_weights = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]

    results = []
    for a, team in enumerate(keys):
        key = f"{match}.{"Blue" if alliance == "b" else "Red"} {a+1}"

        results.append({
                "Key": key,
                "Scouter": random.choice(team_members),
                "Event": tbaEventKey,
                "Level": "qm",
                "Match": match,
                "Alliance": f"{alliance}{a+1}",
                "Team": team.replace("frc", ""),
                "Started With Coral": random.choices([0,1], weights_bool)[0],
                "Left Starting Zone": random.choices([0,1], weights_bool)[0],
                "Auto Level 1": random.choices([0,1,2], auto_coral_weights)[0],
                "Auto Level 2": random.choices([0,1,2], auto_coral_weights)[0],
                "Auto Level 3": random.choices([0,1,2], auto_coral_weights)[0],
                "Auto Level 4": random.choices([0,1,2], auto_coral_weights)[0],
                "Auto Algae Processor": random.choices([0,1,2], [0.8, 0.2, 0.1])[0],
                "Auto Algae Net": random.choices([0,1,2], [0.8, 0.1, 0.1])[0],
                "Tele Level 1": random.choices([0,1,2,3,4,5,6], tele_coral_weights)[0],
                "Tele Level 2": random.choices([0,1,2,3,4,5,6], tele_coral_weights)[0],
                "Tele Level 3": random.choices([0,1,2,3,4,5,6], tele_coral_weights)[0],
                "Tele Level 4": random.choices([0,1,2,3,4,5,6], tele_coral_weights)[0],
                "Tele Algae Processor": random.choices([0,1,2], [0.8, 0.2, 0.1])[0],
                "Tele Algae Net": random.choices([0,1,2], [0.8, 0.2, 0.1])[0],
                "Tele Pickup Coral From": random.choices(["s", "f", "b", "x"])[0],
                "Final Status": random.choices(["p", "s", "d", "x"])[0],
                "Win/Lose": random.choices(["w", "l", "t"])[0],
                "Auto Ranking Point": random.choices([0,1])[0],
                "Coral Ranking Point": random.choices([0,1])[0],
                "Barge Ranking Point": random.choices([0,1])[0],
                "Immobilized": random.choices([0,1])[0],
                "Dropped Game Pieces": random.choices([0,1])[0],
                "Make Good Partner": random.choices([0,1])[0],
                "Comments": "Hello world",
            })
        
    return results

# Load the Matches json and fabricate some scouting data.
def fabricate_data():
    status("Fabricating Scouting Match data...")
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data"))
    filePath = os.path.join(rootPath, f"{tbaEventKey}.matches.json")

    print(filePath)

    # Read the JSON data from the file.
    with open(filePath, "r") as f:
        data = json.load(f)
        data = [row for row in data if row["comp_level"] == "qm"]
        data = sorted(data, key=lambda x: x["match_number"])

    # Create a Pandas DataFrame.
    results = []
    for match, row in enumerate(data):
        match_number = row["match_number"]
        results = results + create_record_for_team(match_number, "b", row["alliances"]["blue"]["team_keys"])
        results = results + create_record_for_team(match_number, "r", row["alliances"]["red"]["team_keys"])

    return results

# Fabricate the data and save it to a file.
results = fabricate_data()
df = pd.DataFrame(results)
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.lower()

csvPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "excel_data"))
df.to_csv(os.path.join(csvPath, f"{tbaEventKey}.tsv"), sep="\t", index=False, header=True)
df.to_csv(os.path.join(csvPath, f"{tbaEventKey}.csv"), sep=",", index=False, header=True)
