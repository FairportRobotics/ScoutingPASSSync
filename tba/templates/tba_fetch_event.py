import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()

# Retrieve values from .env.
tbaEventYear = os.getenv("EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("EVENT_YEAR is not set")

tbaEventKey = os.getenv("TBA_EVENT_KEY")
if tbaEventKey is None:
    raise ValueError("TBA_EVENT_KEY is not set")

tbaAuthKey = os.getenv("TBA_AUTH_KEY")
if tbaAuthKey is None:
    raise ValueError("TBA_AUTH_KEY is not set")

tbaAuthHeader =  {"X-TBA-Auth-Key": tbaAuthKey}

# Define the status function.
def status(message):
    print(f"{datetime.now()}: {message}")

# Make sure the root path exists.
rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data", f"{tbaEventYear}", f"{tbaEventKey}"))
os.makedirs(rootPath, exist_ok=True)


def fetch_event():
    # Prepare the API call.
    status(f"Fetching Event...")
    eventUrl = f"https://www.thebluealliance.com/api/v3/event/{tbaEventKey}"
    tbaEvent = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaEvent = json.loads(tbaEvent.text)

    # Emit a status message based on results of the API call.
    if("Error" in tbaEvent):
        status(f"Fetching Event: '{tbaEventKey}' was not returned")
    else:
        status(f"Fetching Event: '{tbaEvent["short_name"]}'")

    # Log to file.
    filePath = os.path.join(rootPath, f"{tbaEventKey}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaEvent, f, indent=3)

    return tbaEvent

def fetch_teams():
    # Prepare the API call.
    status(f"Fetching Teams...")
    eventUrl = f"https://www.thebluealliance.com/api/v3/event/{tbaEventKey}/teams"
    response = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaTeams = json.loads(response.text)

    # Emit a status message based on results of the API call.
    if("Error" in tbaTeams):
        status(f"Fetching Teams: 0 Teams")
    else:
        status(f"Fetching Teams: {len(tbaTeams)} Teams")    

    # Log to file.
    filePath = os.path.join(rootPath, f"{tbaEventKey}.teams.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaTeams, f, indent=3)    

    return tbaTeams

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
    filePath = os.path.join(rootPath, f"{tbaEventKey}.matches.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaMatches, f, indent=3)

    return tbaMatches

status(f"Fetching data for: {tbaEventKey}")
event = fetch_event()
teams = fetch_teams()
matches = fetch_matches()
