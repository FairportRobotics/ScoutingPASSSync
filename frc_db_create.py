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
        week_number INTEGER,
        code TEXT COLLATE NOCASE NOT NULL,
        name TEXT COLLATE NOCASE NOT NULL,
        type TEXT COLLATE NOCASE,
        venue TEXT COLLATE NOCASE,
        city TEXT COLLATE NOCASE,
        stateprov TEXT COLLATE NOCASE,
        country TEXT COLLATE NOCASE,
        address TEXT COLLATE NOCASE,
        date_start TEXT,
        date_end TEXT
    );

    CREATE UNIQUE INDEX ux_events_year_code ON frc_events (year, code);
    """

    cursor.executescript(command) 


# Retrieve data from FRC.
frc_events()
