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

def retrieveEventsForYear(season):
    status("Retrieving Events from FIRST...")

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{season}/events"
    frcEvents = requests.get(eventUrl, headers=firstAuthHeader)
    frcEvents = json.loads(frcEvents.text)

    # Log to file.
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "frc_data"))
    filePath = os.path.join(rootPath, f"{season}.events.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(frcEvents, f, indent=3)


def retrieveTeamsForYear(season):
    status("Retrieving Teams from FIRST...")

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{season}/teams"
    frcTeams = requests.get(eventUrl, headers=firstAuthHeader)
    frcTeams = json.loads(frcTeams.text)

    # Log to file.
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "frc_data"))
    filePath = os.path.join(rootPath, f"{season}.teams.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(frcTeams, f, indent=3)        
                           

# Retrieve data from FRC.
retrieveEventsForYear(2025)
retrieveTeamsForYear(2025)
status("Complete.")
