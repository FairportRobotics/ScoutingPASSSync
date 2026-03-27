#==================================================================================================
# This script retrieves all the teams which competed with a year.
#==================================================================================================
import datetime
import json
import logging
import os
import requests

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

firstAuthHeader =  {"Authorization": f"Basic {firstAuthKey}", "If-Modified-Since;": ""}


# Make sure the root path exists.
rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data", f"{firstEventYear}"))
os.makedirs(rootPath, exist_ok=True)


# Retrieve the Events for the season then the data associated with each Event.
def fetch_events_for_season():
    status("Fetching Teams from FIRST...")

    all_teams = {"Teams": []}
    page = 1

    status(f"Fetching Teams from FIRST: Page {page}...")
    API_URL = "https://frc-api.firstinspires.org/v3.0/{}/teams?page={}"
    response = requests.get(API_URL.format(firstEventYear, page), headers=firstAuthHeader)
    data = response.json()

    all_teams["Teams"].extend(data["teams"])
    page_total = data["pageTotal"]

    # Log to file.
    filePath = os.path.join(rootPath,  f"_{firstEventYear}",  f"_{firstEventYear}.teams.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(all_teams, f, indent=3)    

    for page in range(2, page_total + 1):
        status(f"Fetching Teams from FIRST: Page {page} of {page_total}...")
        response = requests.get(API_URL.format(firstEventYear, page), headers=firstAuthHeader)
        data = response.json()
        all_teams["Teams"].extend(data["teams"])      

        # Log to file.
        filePath = os.path.join(rootPath,  f"_{firstEventYear}",  f"_{firstEventYear}.teams.json")
        with open(filePath, 'w', newline='') as f:
            json.dump(all_teams, f, indent=3)          


# Retrieve data from FRC.
fetch_events_for_season()
status("Complete.")
