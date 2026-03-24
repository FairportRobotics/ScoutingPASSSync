import json
import os

from datetime import datetime
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()

# Define the status message function.
def status(message):
    print(f"{datetime.now()}: {message}")

# Retrieve values from .env.
tbaEventYear = os.getenv("EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("EVENT_YEAR is not set")

tbaEventKey = os.getenv("TBA_EVENT_KEY")
if tbaEventKey is None:
    raise ValueError("TBA_EVENT_KEY is not set")


# Make sure the root path exists.
rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data", f"{tbaEventYear}", f"{tbaEventKey}"))
os.makedirs(rootPath, exist_ok=True)

# Establish the filenames.
input_file_name = os.path.join(rootPath, f"{tbaEventKey}.matches.json")
ouput_file_name = os.path.join(rootPath, "match.js")


def extract_schedule_from_file(filename):
    status("Reading Match data...")

    # Prepare the array 
    results = []
    with open(filename, "r") as f:
        matches = json.load(f)   

        # Enumerate over the matches.
        for match in matches: 

            # Pull out just the alliances and team keys,
            alliances = {
                "blue": match["alliances"]["blue"]["team_keys"],
                "red": match["alliances"]["red"]["team_keys"],
            }

            # Build the new JSON.
            record = {
                "key": match["key"],
                "match_number": match["match_number"],
                "alliances": alliances
            }

            results.append(record)

    results = sorted(results, key=lambda k: k["match_number"], reverse=False)

    return results


# Define the the function that reads and pushes the Event.
def save_to_javascript(filename, data):
    status("Saving Match data...")

    with open(filename, 'w', newline='') as f:
        output = f"const eventMatches = \n{json.dumps(data, indent=3)};"
        f.write(output)


matches = extract_schedule_from_file(input_file_name)
save_to_javascript(ouput_file_name, matches)
