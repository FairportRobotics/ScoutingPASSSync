from datetime import datetime
import json
import os
import requests
import pandas as pd
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()


# Define the status function.
def status(message):
    print(f"{datetime.now()}: {message}")


# Retrieve values from .env.
tbaAuthKey = os.getenv("TBA_AUTH_KEY")
tbaAuthHeader =  {"X-TBA-Auth-Key": tbaAuthKey}
if tbaAuthKey is None:
    raise ValueError("TBA_AUTH_KEY is not set")

tbaEventYear = os.getenv("TBA_EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("TBA_EVENT_YEAR is not set")


# Make sure the path to the correct Game Year exists.
current_directory = os.path.dirname(os.path.abspath(__file__))
target_year_directory = os.path.join(current_directory, "Game Years", tbaEventYear)
os.makedirs(target_year_directory, exist_ok=True)


def fetch_events_for_year():
    # Prepare the API call.
    status(f"Fetching events for: {tbaEventYear}")
    eventUrl = f"https://www.thebluealliance.com/api/v3/events/{tbaEventYear}"
    tbaEvent = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaEvent = json.loads(tbaEvent.text)

    # Log to file.
    filePath = os.path.join(target_year_directory, f"{tbaEventYear}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaEvent, f, indent=3)

    return tbaEvent


fetch_events_for_year()