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
# Retrieve values from .env.
firstEventYear = os.getenv("FIRST_EVENT_YEAR")
if firstEventYear is None:
    raise ValueError("FIRST_EVENT_YEAR is not set")

firstAuthKey = os.getenv("FIRST_AUTH_KEY")
if firstAuthKey is None:
    raise ValueError("FIRST_AUTH_KEY is not set")

firstAuthHeader =  {"Authorization": f"Basic {firstAuthKey}"}


# Make sure the root path exists.
rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data", f"{firstEventYear}"))
os.makedirs(rootPath, exist_ok=True)


# Retrieve the Events for the season then the data associated with each Event.
def fetch_events_for_season():
    status("Fetching Events from FIRST...")

    # Prepare the API call.
    url = f"https://frc-api.firstinspires.org/v3.0/{firstEventYear}/events"
    frcEvents = requests.get(url, headers=firstAuthHeader)
    frcEvents = json.loads(frcEvents.text)

    # Log to file.
    filePath = os.path.join(rootPath, f"{firstEventYear}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(frcEvents, f, indent=3)

    return frcEvents

# Retrieve data from FRC.
fetch_events_for_season()
status("Complete.")
