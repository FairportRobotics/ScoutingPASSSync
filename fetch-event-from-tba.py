from datetime import datetime
import json
import os
import requests
import pandas as pd
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()

# Retrieve values from .env.
tbaEventKey: str = os.getenv("TBA_EVENT_KEY")   # From FIRST/The Blue Alliance
tbaAuthKey: str = os.getenv("TBA_AUTH_KEY")     # From The Blue Alliance
tbaAuthHeader =  {"X-TBA-Auth-Key": tbaAuthKey}

# Define the status function.
def status(message):
    print(f"{datetime.now()}: {message}")

# Validate arguments.
if tbaEventKey == "":
    status("No event key provided.")
    exit()

if tbaAuthKey == "":
    status("No TBA Auth key provided.")
    exit()    


def fetch_event():
    # Prepare the API call.
    status(f"Fetching event...")
    eventUrl = "https://www.thebluealliance.com/api/v3/event/" + tbaEventKey
    tbaEvent = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaEvent = json.loads(tbaEvent.text)

    # Log to file.
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "tba_data"))
    filePath = os.path.join(rootPath, f"{tbaEventKey}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaEvent, f, indent=3)

    return tbaEvent

def fetch_teams():
    # Prepare the API call.
    status(f"Fetching teams...")
    eventUrl = "https://www.thebluealliance.com/api/v3/event/" + tbaEventKey + "/teams"
    response = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaTeams = json.loads(response.text)

    # Log to file.
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "tba_data"))
    filePath = os.path.join(rootPath, f"{tbaEventKey}.teams.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaTeams, f, indent=3)    

    return tbaTeams

def fetch_matches():
    # Prepare the API call.
    status(f"Fetching matches...")
    eventUrl = "https://www.thebluealliance.com/api/v3/event/" + tbaEventKey + "/matches"
    tbaMatches = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaMatches = json.loads(tbaMatches.text)

    # Log to file.
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "tba_data"))
    filePath = os.path.join(rootPath, f"{tbaEventKey}.matches.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaMatches, f, indent=3)

    return tbaMatches

status(f"Fetching data for: {tbaEventKey}")
event = fetch_event()
teams = fetch_teams()
matches = fetch_matches()

status(f"Event: {event['key']}, {event['name']}")
status(f"Teams: {len(teams)}")
status(f"Matches: {len(matches)}")   
