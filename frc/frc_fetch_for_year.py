#==================================================================================================
# This script flushes and fills the Event, Matches and Teams associated with a competition.
# FIRST_EVENT_KEY="NYRoc"
#
# https://frc-api.firstinspires.org/v3.0/:season/events?eventCode=&teamNumber=&districtCode=&excludeDistrict=&weekNumber&tournamentType
# FIRST_AUTH_KEY="ZmFpcnBvcnRyb2JvdGljczo5ZmFjOTUwMi00ODkxLTQ0MzUtOTBhNi0yYjkwMjkwY2E0YWU="
#==================================================================================================
import datetime
import json
import logging
import os
import requests
import pandas as pd
from pathlib import Path

from datetime import datetime
from dotenv import load_dotenv              

# Load the .env file and all environment variables.
load_dotenv()

# Set the logging format.
def status(message):
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: {message}")

# Set the logging level.
logging.getLogger("httpx").setLevel(logging.WARNING)

# Retrieve values from .env.
firstAuthKey: str = os.getenv("FIRST_AUTH_KEY")     # From FIRST
firstAuthHeader =  {"Authorization": f"Basic {firstAuthKey}"}

season = 2025

def save_file_to_subfolder(subfolder, filename, content):
    # Get the directory of the running script
    script_dir = Path(__file__).parent  

    # Define and create the folder
    folder_path = script_dir / subfolder
    folder_path.mkdir(parents=True, exist_ok=True)

    # Construct the full file path
    file_path = os.path.join(folder_path, filename)

    # Save the content to the file
    with open(file_path, 'w') as f:
        f.write(content)


# Retrieve the Events for the season then the data associated with each Event.
def fetch_events_for_season():
    status("Fetching Events from FIRST...")

    # Prepare the API call.
    url = f"https://frc-api.firstinspires.org/v3.0/{season}/events"
    frcEvents = requests.get(url, headers=firstAuthHeader)
    frcEvents = json.loads(frcEvents.text)

    # Log to file.
    save_file_to_subfolder("data", f"{season}.teams.json", json.dumps(frcEvents, indent=3))

    # Enumerate over the Events to retrieve the Matches and Results.
    for e_index, event in enumerate(frcEvents["Events"]):
        # Display a status for the event.
        eventCode = event["code"]
        status(f"Processing Event {e_index+1} of {len(frcEvents['Events'])}: {eventCode}")

        # Save the Event to file.
        save_file_to_subfolder("data", f"{season}.{eventCode}.event.json", json.dumps(event, indent=3))

        # Retrieve the Schedule and save to file.
        status(f"   Fetching Schedule...")
        level = "Qualification"
        url = f"https://frc-api.firstinspires.org/v3.0/{season}/schedule/{eventCode}?tournamentLevel={level}"
        frcMatches = requests.get(url, headers=firstAuthHeader)
        frcMatches = json.loads(frcMatches.text)
        save_file_to_subfolder("data", f"{season}.{eventCode}.schedule.json", json.dumps(frcMatches, indent=3))

        # Retrieve the Results and save to file.
        status(f"   Fetching Results...")
        url = f"https://frc-api.firstinspires.org/v3.0/{season}/scores/{eventCode}/Qualification"
        frcResults = requests.get(url, headers=firstAuthHeader)
        frcResults = json.loads(frcResults.text)
        save_file_to_subfolder("data", f"{season}.{eventCode}.results.json", json.dumps(frcResults, indent=3))

        # Retrieve the Teams
        status(f"   Fetching Teams...")
        #https://frc-api.firstinspires.org/v3.0/:season/teams?teamNumber=&eventCode=&districtCode=&state=&page=
        url = f"https://frc-api.firstinspires.org/v3.0/{season}/teams?eventCode={eventCode}"
        frcTeams = requests.get(url, headers=firstAuthHeader)
        frcTeams = json.loads(frcTeams.text)
        save_file_to_subfolder("data", f"{season}.{eventCode}.teams.json", json.dumps(frcTeams, indent=3))        

# Retrieve data from FRC.
fetch_events_for_season()
status("Complete.")
