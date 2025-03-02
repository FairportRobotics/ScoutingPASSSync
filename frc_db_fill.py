import sqlite3
import datetime
import json
import logging
import os
import requests
import pandas as pd
from datetime import datetime

connection = sqlite3.connect("frc.db")
cursor = connection.cursor()

# Enable foreign key constraints
connection.execute('PRAGMA foreign_keys = ON;')

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
    #print(records)

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



# Retrieve data from FRC.
frcEventsFill(2025)
frcTeamsFill(2025)
