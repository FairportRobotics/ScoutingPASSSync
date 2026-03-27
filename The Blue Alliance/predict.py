import json
import os
import json
import os
import requests

from datetime import datetime
from dotenv import load_dotenv 

# Define the status message function.
def status(message):
    print(f"{datetime.now()}: {message}")


# Load the .env file and all environment variables.
load_dotenv()

# Retrieve values from .env.
tbaAuthKey = os.getenv("TBA_AUTH_KEY")
tbaAuthHeader =  {"X-TBA-Auth-Key": tbaAuthKey}
if tbaAuthKey is None:
    raise ValueError("TBA_AUTH_KEY is not set")

tbaEventYear = os.getenv("TBA_EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("TBA_EVENT_YEAR is not set")

tbaEventKey = os.getenv("TBA_EVENT_KEY")
if tbaEventKey is None:
    raise ValueError("TBA_EVENT_KEY is not set")

status(f"Processing {tbaEventKey}")

# Define folder paths.
current_directory = os.path.dirname(os.path.abspath(__file__))
target_event_directory = os.path.join(current_directory, "Game Years", tbaEventYear, tbaEventKey)
template_directory = os.path.join(current_directory, "Templates")
os.makedirs(target_event_directory, exist_ok=True)


# Retrieve most recent match data from TBA.
def fetch_matches():
    # Prepare the API call.
    status(f"Fetching Matches...")
    eventUrl = f"https://www.thebluealliance.com/api/v3/event/{tbaEventKey}/matches"
    tbaMatches = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaMatches = json.loads(tbaMatches.text)

    # Emit a status message based on results of the API call.
    if("Error" in tbaMatches):
        status(f"Fetching Matches: 0 Matches")
    else:
        status(f"Fetching Matches: {len(tbaMatches)} Matches")      

    # Log to file.
    filePath = os.path.join(target_event_directory, f"{tbaEventKey}.matches.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaMatches, f, indent=3)

    return tbaMatches


