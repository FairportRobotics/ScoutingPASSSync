#==================================================================================================
# This script retrieves all events for a specific year, then enumerates those events and fetches
# the Qualification match results for each event.
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
rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data", f"{firstEventYear}", "_2025"))
os.makedirs(rootPath, exist_ok=True)

# Retrieve the Events for the season then the data associated with each Event.
def do_something():

    # Prepare the API call.
    url = f"https://frc-api.firstinspires.org/v3.0/{firstEventYear}"
    results = requests.get(url, headers=firstAuthHeader)
    status(results)

do_something()