from datetime import datetime
import json
import os
import requests
import pandas as pd
from dotenv import load_dotenv 


# Load the .env file and all environment variables.
load_dotenv()

# Retrieve values from .env.
tbaEventYear = os.getenv("EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("EVENT_YEAR is not set")

tbaAuthKey = os.getenv("TBA_AUTH_KEY")
if tbaAuthKey is None:
    raise ValueError("TBA_AUTH_KEY is not set")

tbaAuthHeader =  {"X-TBA-Auth-Key": tbaAuthKey}

# Make sure the root path exists.
rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data"))
os.makedirs(rootPath, exist_ok=True)

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
    eventUrl = f"https://www.thebluealliance.com/api/v3/events/{tbaEventYear}"
    tbaEvent = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaEvent = json.loads(tbaEvent.text)

    # Log to file.
    filePath = os.path.join(rootPath, f"{tbaEventYear}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaEvent, f, indent=3)

    return tbaEvent


status(f"Fetching events for: {tbaEventYear}")
fetch_events()