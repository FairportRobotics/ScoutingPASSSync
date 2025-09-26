#==================================================================================================
# This script flushes and fills the Event, Matches and Teams associated with a competition.
# FIRST_EVENT_KEY="NYRoc"
#
# https://frc-api-docs.firstinspires.org/#1ca9c544-9112-4a28-b654-aec7933bb9c0
# FIRST_AUTH_KEY="ZmFpcnBvcnRyb2JvdGljczo5ZmFjOTUwMi00ODkxLTQ0MzUtOTBhNi0yYjkwMjkwY2E0YWU="
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
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')} - {message}")

# Set the logging level.
logging.getLogger("httpx").setLevel(logging.WARNING)

# Retrieve values from .env.
firstEventKey = os.getenv("FIRST_EVENT_KEY")
if firstEventKey is None:
    raise ValueError("FIRST_EVENT_KEY is not set")

firstEventYear = os.getenv("FIRST_EVENT_YEAR")
if firstEventYear is None:
    raise ValueError("FIRST_EVENT_YEAR is not set")

firstAuthKey = os.getenv("FIRST_AUTH_KEY")
if firstAuthKey is None:
    raise ValueError("FIRST_AUTH_KEY is not set")

firstAuthHeader =  {"Authorization": f"Basic {firstAuthKey}"}

# Make sure the root path exists.
rootPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "data", f"{firstEventYear}", f"{firstEventKey}"))
os.makedirs(rootPath, exist_ok=True)


def retrieveEventFromFirst(firstEventKey):
    status("Retrieving Event from FIRST...")

    # Validate argument.
    if firstEventKey == "":
        return

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{firstEventYear}/events?eventCode={firstEventKey}"
    firstEvent = requests.get(eventUrl, headers=firstAuthHeader)
    firstEvent = json.loads(firstEvent.text)
    firstEvent = firstEvent["Events"][0]

    # Log to file.
    filePath = os.path.join(rootPath, f"{firstEventYear}.{firstEventKey}.event.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(firstEvent, f, indent=3)


def retrieveMatchesFromFirst(firstEventKey):
    status("Retrieving Matches from FIRST...")

    # Validate argument.
    if firstEventKey == "":
        return
    
    # Definine the tournament level.
    level = "Qualification"
    #level = "Playoff"

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{firstEventYear}/schedule/{firstEventKey}?tournamentLevel={level}"
    firstMatches = requests.get(eventUrl, headers=firstAuthHeader)
    firstMatches = json.loads(firstMatches.text)
    firstMatches = firstMatches["Schedule"]

    # Log to file.
    filePath = os.path.join(rootPath, f"{firstEventYear}.{firstEventKey}.matches.{level}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(firstMatches, f, indent=3)


def retrieveTeamsFromFirst(firstEventKey):
    status("Retrieving Teams from FIRST...")

    # Validate argument.
    if firstEventKey == "":
        return

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{firstEventYear}/teams?eventCode={firstEventKey}"
    firstTeams = requests.get(eventUrl, headers=firstAuthHeader)
    firstTeams = json.loads(firstTeams.text)
    firstTeams = firstTeams["teams"] 
    
    # Log to file.
    filePath = os.path.join(rootPath, f"{firstEventYear}.{firstEventKey}.teams.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(firstTeams, f, indent=3)


#https://frc-api.firstinspires.org/v3.0/:season/scores/:eventCode/:tournamentLevel?matchNumber=&start=&end=
def retrieveResultsFromFirst(firstEventKey):
    status("Retrieving Results from FIRST...")

    # Validate argument.
    if firstEventKey == "":
        return

    # Prepare the API call.
    eventUrl = f"https://frc-api.firstinspires.org/v3.0/{firstEventYear}/scores/{firstEventKey}/Qualification"
    matchResults = requests.get(eventUrl, headers=firstAuthHeader)
    matchResults = json.loads(matchResults.text)

    # Log to file.
    filePath = os.path.join(rootPath, f"{firstEventYear}.{firstEventKey}.results.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(matchResults, f, indent=3)
                               

# Retrieve data from FRC.
retrieveEventFromFirst(firstEventKey)
retrieveMatchesFromFirst(firstEventKey)
retrieveTeamsFromFirst(firstEventKey)
retrieveResultsFromFirst(firstEventKey)
status("Complete.")
