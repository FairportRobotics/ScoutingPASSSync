import sqlite3
import datetime
import json
import requests
import os
from datetime import datetime
from pathlib import Path

# Get the directory of the running script
script_dir = Path(__file__).parent  
file_path = script_dir / "frc.db"

connection = sqlite3.connect(file_path)
cursor = connection.cursor()

# Enable foreign key constraints
connection.execute('PRAGMA foreign_keys = ON;')

# Retrieve values from .env.
firstAuthKey: str = os.getenv("FIRST_AUTH_KEY")     # From FIRST
firstAuthHeader =  {"Authorization": f"Basic {firstAuthKey}"}


# Define the season. Note that each years results will result in a differnt schema so perhaps this 
# script should named specific to Reefscape.
season = 2025


# Set the logging format.
def status(message):
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: {message}")


# Flush/delete existing data.
def flush_existing_data():
    # Perform bulk insert
    command = """
        DELETE FROM frc_teams;
        DELETE FROM frc_match_teams;
        DELETE FROM frc_matches;
        DELETE FROM frc_events;
    """
    cursor.executescript(command)
    connection.commit()    


# Retrieve the cached Events and populate tables.
def frc_events_fill():
    status("Populating table: frc_events")

    # Read the JSON data from the file.
    file_path = script_dir / f"data/{season}.events.json"
    with open(file_path, "r") as f:
        data = json.load(f)

    events = data["Events"]

    # Prepare the list of tuples for bulk insert
    records = [(f"{season}.{event["code"]}", season, event["weekNumber"], event["code"], event["name"], event["type"], event["venue"], event["city"], event["stateprov"], event["country"], event["address"], event["dateStart"], event["dateEnd"]) for event in events]

    # Perform bulk insert
    command = """
        INSERT INTO frc_events (key, year, weekNumber, code, name, type, venue, city, stateprov, country, address, dateStart, dateEnd)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (year, code) DO NOTHING;
    """
    cursor.executemany(command, records)
    connection.commit()

    # Enumerate over the events and load the associated tables.
    for ei, event in enumerate(events):
        eventCode = event["code"]
        eventKey = f"{season}.{event["code"]}"
        status(f"Processing {eventCode}...")
        frc_teams_fill(eventCode)
        frc_matches_fill(eventCode, eventKey)
        status(f"   Loading frc_match_teams...")
        status(f"   Loading frc_teams...")



"""
{
    "teamNumber": 1,
    "nameFull": "FCA Foundation/Molex/3M&Oakland Schools Technical Campus Northeast",
    "nameShort": "The Juggernauts",
    "city": "Pontiac",
    "stateProv": "Michigan",
    "country": "USA",
    "rookieYear": 1997,
    "robotName": "",
    "districtCode": "FIM",
    "schoolName": "Oakland Schools Technical Campus Northeast",
    "website": "",
    "homeCMP": null
},
"""
def frc_teams_fill(eventCode):
    status("   Loading frc_teams...")

    # Read the JSON data from the file.
    file_path = script_dir / f"data/{season}.{eventCode}.teams.json"
    with open(file_path, "r") as f:
        data = json.load(f)  

    teams = data["teams"]

    # Prepare the list of tuples for bulk insert
    records = [(team["teamNumber"], team["nameShort"], team["nameFull"], team["city"], team["stateProv"], team["country"], team["rookieYear"], team["robotName"], team["districtCode"], team["schoolName"], team["website"]) for team in teams]

    # Perform bulk insert
    command = """
        INSERT INTO frc_teams (teamNumber, nameShort, nameFull, city, stateProv, country, rookieYear, robotName, districtCode, schoolName, website) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        ON CONFLICT (teamNumber) DO NOTHING;
    """
    cursor.executemany(command, records)
    connection.commit()


def frc_matches_fill(eventCode, eventKey):
    status("   Loading frc_matches and frc_match_teams...")

    # Read the JSON data from the file.
    file_path = script_dir / f"data/{season}.{eventCode}.schedule.json"
    with open(file_path, "r") as f:
        data = json.load(f)  

    frcMatches = data["Schedule"]

    # Create a dictionary so we can extract the station components.
    alliance = {
        "Red1": {"alliance": "Red", "number": 1},
        "Red2": {"alliance": "Red", "number": 2},
        "Red3": {"alliance": "Red", "number": 3},
        "Blue1": {"alliance": "Blue", "number": 1},
        "Blue2": {"alliance": "Blue", "number": 2},
        "Blue3": {"alliance": "Blue", "number": 3},
    }        

    for mi, match in enumerate(frcMatches):
        # Prepare the list of tuples for bulk insert
        matchKey = f"{season}.{eventCode}.{ match["tournamentLevel"]}.{match["matchNumber"]}"

        # Perform bulk insert of Match records.
        matchRecords = [(matchKey, eventKey, season, eventCode, match["tournamentLevel"], match["matchNumber"], match["startTime"], match["description"], match["field"])]
        cursor.executemany("INSERT INTO frc_matches (key, eventKey, year, code, tournamentLevel, matchNumber, startTime, description, field) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (key) DO NOTHING;", matchRecords)

        # Perform bulk insert of Match Team records.
        teamRecords = [(matchKey, team["station"], alliance[team["station"]]["alliance"], alliance[team["station"]]["number"], team["teamNumber"], team["surrogate"]) for team in match["teams"]]
        cursor.executemany("INSERT INTO frc_match_teams (matchKey, station, alliance, number, teamNumber, surrogate) VALUES (?, ?, ?, ?, ?, ?);", teamRecords)
        connection.commit()
    

# Load and retrieve data from FRC.
flush_existing_data()
frc_events_fill()
#frc_teams_fill()
#frcTeamsFill(2025)
#frcFillMatchesAndMatchTeams(2025)
