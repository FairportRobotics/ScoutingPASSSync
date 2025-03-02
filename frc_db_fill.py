import sqlite3
import datetime
import json
import requests
import os
from datetime import datetime

connection = sqlite3.connect("frc.db")
cursor = connection.cursor()

# Enable foreign key constraints
connection.execute('PRAGMA foreign_keys = ON;')

# Retrieve values from .env.
firstAuthKey: str = os.getenv("FIRST_AUTH_KEY")     # From FIRST
firstAuthHeader =  {"Authorization": f"Basic {firstAuthKey}"}

# Set the logging format.
def status(message):
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')} - {message}")

"""
{
    "allianceCount": "EightAlliance",
    "weekNumber": 2,
    "announcements": [],
    "code": "NYSU",
    "divisionCode": null,
    "name": "Hudson Valley Regional",
    "type": "Regional",
    "districtCode": null,
    "venue": "Rockland Community College - Athletic Center",
    "city": "Suffern",
    "stateprov": "NY",
    "country": "USA",
    "dateStart": "2025-03-05T00:00:00",
    "dateEnd": "2025-03-08T23:59:59",
    "address": "145 College Road",
    "website": "https://www.nysfirst.org/",
    "webcasts": [
    "https://www.twitch.tv/firstinspires9"
    ],
    "timezone": "Eastern Standard Time"
},
"""
def frcEventsFill(season):
    status("Populating table: frc_events")

    # Read the JSON data from the file.
    file=f"frc_data/{season}.events.json"
    with open(file, "r") as f:
        data = json.load(f)

    events = data["Events"]

    # Prepare the list of tuples for bulk insert
    records = [(season, event["weekNumber"], event["code"], event["name"], event["type"], event["venue"], event["city"], event["stateprov"], event["country"], event["address"], event["dateStart"], event["dateEnd"]) for event in events]

    # Perform bulk insert
    cursor.executemany("INSERT INTO frc_events (year, weekNumber, code, name, type, venue, city, stateprov, country, address, dateStart, dateEnd) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (year, code) DO NOTHING;", records)
    connection.commit()

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
def frcTeamsFill(season):
    status("Populating table: frc_teams")

    # Read the JSON data from the file.
    file=f"frc_data/{season}.teams.json"
    with open(file, "r") as f:
        data = json.load(f)

    events = data["teams"]

    # Prepare the list of tuples for bulk insert
    records = [(event["teamNumber"], event["nameFull"], event["nameShort"], event["city"], event["stateProv"], event["country"], event["rookieYear"], event["robotName"], event["districtCode"], event["schoolName"], event["website"]) for event in events]

    # Perform bulk insert
    cursor.executemany("INSERT INTO frc_teams (teamNumber, nameFull, nameShort, city, stateProv, country, rookieYear, robotName, districtCode, schoolName, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (teamNumber) DO NOTHING;", records)
    connection.commit()


"""
key TEXT PRIMARY KEY,
year INTEGER NOT NULL,
code TEXT COLLATE NOCASE NOT NULL,
tournamentLevel TEXT COLLATE NOCASE NOT NULL,
matchNumber INTEGER NOT NULL,
startTime TEXT,
description TEXT COLLATE NOCASE,
field TEXT COLLATE NOCASE


matchKey TEXT COLLATE NOCASE NOT NULL,
station INTEGER NOT NULL,
teamNumber INTEGER NOT NULL,
surrogate BOOLEAN NOT NULL,
FOREIGN KEY (matchKey) REFERENCES frc_matches (key),
FOREIGN KEY (teamNumber) REFERENCES frc_teams (teamNumber)
"""
def frcEventsEnumerate(season):
    status("Populating table: frc_matches")

    # Read the JSON data from the file.
    file=f"frc_data/{season}.events.json"
    with open(file, "r") as f:
        data = json.load(f)

    frcEvents = data["Events"]
    for ei, event in enumerate(frcEvents):
        print(f"Processing Event {ei+1} of {len(frcEvents)}: {event['code']}")

        # Definine the tournament level.
        level = "Qualification"
        #level = "Playoff"

        # Prepare the API call.
        eventUrl = f"https://frc-api.firstinspires.org/v3.0/{season}/schedule/{event["code"]}?tournamentLevel={level}"
        frcMatches = requests.get(eventUrl, headers=firstAuthHeader)
        frcMatches = json.loads(frcMatches.text)
        frcMatches = frcMatches["Schedule"]

        for mi, match in enumerate(frcMatches):
            print(f"   Processing Match {mi+1} of {len(frcMatches)}: {match['matchNumber']}")

            # Prepare the list of tuples for bulk insert
            matchKey = f"{season}.{event["code"]}.{ match["tournamentLevel"][0]}.{match["matchNumber"]}"

            # Perform bulk insert of Match records.
            matchRecords = [(matchKey, season, event["code"], match["tournamentLevel"], match["matchNumber"], match["startTime"], match["description"], match["field"])]
            cursor.executemany("INSERT INTO frc_matches (key, year, code, tournamentLevel, matchNumber, startTime, description, field) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (key) DO NOTHING;", matchRecords)

            # Perform bulk insert of Match Team records.
            teamRecords = [(matchKey, team["station"], team["teamNumber"], team["surrogate"]) for team in match["teams"]]
            cursor.executemany("INSERT INTO frc_match_teams (matchKey, station, teamNumber, surrogate) VALUES (?, ?, ?, ?);", teamRecords)
            connection.commit()
    

# Load and retrieve data from FRC.
frcEventsFill(2025)
frcTeamsFill(2025)
frcEventsEnumerate(2025)
