import json
import os
import random
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()

# Define the status function.
def status(message):
    print(f"{datetime.now()}: {message}")


# Retrieve values from .env.
tbaEventYear = os.getenv("TBA_EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("TBA_EVENT_YEAR is not set")

tbaEventKey = os.getenv("TBA_EVENT_KEY")
if tbaEventKey is None:
    raise ValueError("TBA_EVENT_KEY is not set")


# Define folder paths.
current_directory = os.path.dirname(os.path.abspath(__file__))
target_event_directory = os.path.join(current_directory, "Game Years", tbaEventYear, tbaEventKey)
os.makedirs(target_event_directory, exist_ok=True)


team_members = [
    "Dean Blanchard ",
    "Rachel Case ",
    "Ruth Christensen ",
    "Andrew Crawford  ",
    "Gianmarco D'Angelo  ",
    "Vaishu Das ",
    "Madison DeCicca ",
    "Nathan DeVito ",
    "Domenic Giammusso ",
    "Eli Harrison ",
    "Tyler Hignett ",
    "Runa Hunt ",
    "Colby Jackson ",
    "Matthew Mazzota ",
    "Caitlin Munier ",
    "Nicholas Munier ",
    "Celton Norter ",
    "Amanah Obaji ",
    "Connor Rapp ",
    "Arthur Sayre ",
    "Autumn Schoenfeld ",
    "Mason Silva ",
    "Carter Silva ",
    "Ethan Stiffler ",
    "Tetra Ukav ",
    "Kai  Wilbur ",
    "Jonah Woika "
]


# Define a function that accepts the match number, the alliance, and the team keys.
# This function will fabricate scouting data for each team in the alliance.
def create_record_for_team(match, alliance, keys):
    results = []
    for a, team in enumerate(keys):
        key = f"{match}.{"Blue" if alliance == "b" else "Red"} {a+1}"

        results.append({
            "Key": key,
            "Scouter": random.choice(team_members),
            "Match": match,
            "Alliance": f"{alliance}{a+1}",
            "Team": team.replace("frc", ""),

            "Robot Move in Auto": random.choices([0,1])[0],
            "A-Stop Activated": random.choices([-1, 0,1])[0],
            "Total Fuel Scored": random.choices([1, 2, 3, 4, 5])[0],
            
            "Speed to Shoot Fuel": random.choices([1, 2, 3])[0],
            "Accuracy to Shoot Fuel": random.choices([1, 2, 3])[0],
            "Number of Fuel Scored": random.choices([1, 2, 3, 4, 5])[0],
            "Collect from Neutral Zone": random.choices([0,1])[0],
            "Collect from Alliance Zone": random.choices([0,1])[0],
            "Did relay Fuel": random.choices([0,1])[0],
            "TDid bulldoze Fuel": random.choices([0,1])[0],
            "Was Intake Good": random.choices([0,1])[0],
            
            "Defensive Whole Game": random.choices([0,1])[0],
            "Shot from Same Position": random.choices([0,1])[0],
            "Grade Robot's Performance": random.choices([-1, 1, 2, 3, 4])[0],

            "Result of Match": random.choices([-1, 0, 1])[0],
            "Energized Ranking Point": random.choices([0,1])[0],
            "Supercharged Ranking Point": random.choices([0,1])[0],
            "Traversal Ranking Point": random.choices([0,1])[0],
            "Total Points Scored": random.randint(25,500),
            "Comments": "Hello World!",
        })
        
    return results

# Load the Matches json and fabricate some scouting data.
def fabricate_data_from_matches():
    status("Fabricating Scouting Match data...")
    filePath = os.path.join(target_event_directory, f"{tbaEventKey}.matches.json")

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
results = fabricate_data_from_matches()
df = pd.DataFrame(results)
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.lower()

df.to_csv(os.path.join(target_event_directory, f"{tbaEventKey}.fake-data.tsv"), sep="\t", index=False, header=True)
df.to_csv(os.path.join(target_event_directory, f"{tbaEventKey}.fake-data.csv"), sep=",", index=False, header=True)
