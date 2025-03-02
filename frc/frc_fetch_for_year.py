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
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')} - {message}")

# Set the logging level.
logging.getLogger("httpx").setLevel(logging.WARNING)

# Retrieve values from .env.
firstAuthKey: str = os.getenv("FIRST_AUTH_KEY")     # From FIRST
firstAuthHeader =  {"Authorization": f"Basic {firstAuthKey}"}

season = 2025

def save_file_to_subfolder(filename, content, subfolder):
    # Create the subfolder if it doesn't exist
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), subfolder))
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # Construct the full file path
    file_path = os.path.join(subfolder, filename)

    # Save the content to the file
    with open(file_path, 'w') as f:
        f.write(content)

def fetch_events_for_season():
    status("Fetching Events from FIRST...")

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{season}/events"
    frcEvents = requests.get(eventUrl, headers=firstAuthHeader)
    frcEvents = json.loads(frcEvents.text)

    # Log to file.
    save_file_to_subfolder(f"{season}.teams.json", json.dumps(frcEvents, indent=3), "data")

    # Enumerate over the Events to retrieve the Matches and Results.
    for e_index, event in enumerate(frcEvents["Events"]):
        eventCode = event["code"]
        status(f"Processing Event {e_index+1} of {len(frcEvents['Events'])}: {eventCode}")

        # Save the Event to file.
        save_file_to_subfolder(f"{season}.{eventCode}.event.json", json.dumps(event, indent=3), "data")

        # Retrieve the Schedule.
        level = "Qualification"
        eventUrl = f"https://frc-api.firstinspires.org/v3.0/{season}/schedule/{eventCode}?tournamentLevel={level}"
        frcMatches = requests.get(eventUrl, headers=firstAuthHeader)
        frcMatches = json.loads(frcMatches.text)

        # Log to file.
        save_file_to_subfolder(f"{season}.{eventCode}.schedule.json", json.dumps(frcMatches, indent=3), "data")

        # Retrieve the Results.
        eventUrl = f"https://frc-api.firstinspires.org/v3.0/{season}/scores/{eventCode}/Qualification"
        frcResults = requests.get(eventUrl, headers=firstAuthHeader)
        frcResults = json.loads(frcResults.text)

        # Log to file.
        save_file_to_subfolder(f"{season}.{eventCode}.results.json", json.dumps(frcResults, indent=3), "data")        


def fetch_teams_for_season():
    status("Fetching Teams from FIRST...")

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{season}/teams"
    frcTeams = requests.get(eventUrl, headers=firstAuthHeader)
    frcTeams = json.loads(frcTeams.text)

    # Log to file.
    save_file_to_subfolder(f"{season}.teams.json", json.dumps(frcTeams, indent=3), "data")
                           

# Retrieve data from FRC.
fetch_events_for_season()
fetch_teams_for_season()
status("Complete.")
