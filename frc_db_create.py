import sqlite3
import datetime
import json
import logging
import os
import requests
import pandas as pd

from dotenv import load_dotenv  
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
def frc_events():
    status("Creating table: frc_events")

    command = """
    DROP TABLE IF EXISTS frc_events;

    CREATE TABLE frc_events (
        year INTEGER NOT NULL,
        weekNumber INTEGER,
        code TEXT COLLATE NOCASE NOT NULL,
        name TEXT COLLATE NOCASE NOT NULL,
        type TEXT COLLATE NOCASE,
        venue TEXT COLLATE NOCASE,
        city TEXT COLLATE NOCASE,
        stateprov TEXT COLLATE NOCASE,
        country TEXT COLLATE NOCASE,
        address TEXT COLLATE NOCASE,
        dateStart TEXT,
        dateEnd TEXT
    );

    CREATE UNIQUE INDEX ux_events_year_code ON frc_events (year, code);
    """

    cursor.executescript(command) 


"""
{
    "teamNumber": 245,
    "nameFull": "General Motors/Aptiv/State of MI/Molex/Salem Steel/Thyssenkrupp/R & G Drummer/Stellantis/Fanuc/Tek Pros Today/Chris Pickard/Adambots Friends & Family/Rochester Advanced Dentistry/Thyssenkrupp Plastics&Adams High School",
    "nameShort": "Adambots",
    "city": "Rochester Hills",
    "stateProv": "Michigan",
    "country": "USA",
    "rookieYear": 1999,
    "robotName": "",
    "districtCode": "FIM",
    "schoolName": "Adams High School",
    "website": "",
    "homeCMP": null
},
"""    
def frc_teams():
    status("Creating table: frc_teams")

    command = """
    DROP TABLE IF EXISTS frc_teams;

    CREATE TABLE frc_teams (
        teamNumber INTEGER PRIMARY KEY,
        nameFull TEXT COLLATE NOCASE NOT NULL,
        nameShort TEXT COLLATE NOCASE NOT NULL,
        city TEXT COLLATE NOCASE NOT NULL,
        stateProv TEXT COLLATE NOCASE NOT NULL,
        country TEXT COLLATE NOCASE NOT NULL,
        rookieYear INTEGER,
        robotName TEXT COLLATE NOCASE,
        districtCode TEXT COLLATE NOCASE,
        schoolName TEXT COLLATE NOCASE,
        website TEXT COLLATE NOCASE
    );
    """

    cursor.executescript(command) 

# Create the tables.
frc_events()
frc_teams()
