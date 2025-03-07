from datetime import datetime
import json
import os
import requests
import pandas as pd
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()

# Retrieve values from .env.
tbaEventYear: str = os.getenv("EVENT_YEAR")   # From FIRST/The Blue Alliance
tbaAuthKey: str = os.getenv("TBA_AUTH_KEY")     # From The Blue Alliance
tbaAuthHeader =  {"X-TBA-Auth-Key": tbaAuthKey}

# Define the status function.
def status(message):
    print(f"{datetime.now()}: {message}")

# Validate arguments.
if tbaEventYear == "":
    status("No event year provided.")
    exit()

if tbaAuthKey == "":
    status("No TBA Auth key provided.")
    exit()     


def fetch_events():
    # Prepare the API call.
    eventUrl = "https://www.thebluealliance.com/api/v3/events/" + tbaEventYear
    tbaEvent = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaEvent = json.loads(tbaEvent.text)

    # Log to file.
    rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data"))
    filePath = os.path.join(rootPath, f"{tbaEventYear}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaEvent, f, indent=3)

    return tbaEvent


status(f"Fetching events for: {tbaEventYear}")
fetch_events()