# Calling The Blue Alliance API and Pushing into Excel Spreadsheets

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#tba">Purpose</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#how-to-use">How to Use</a></li>
    <li><a href="#scripts">Scripts</a></li>
    <li><a href="#todo">Todo</a></li>
  </ol>
</details>

<!-- Purpose -->
<div id="purpose"></div>

## Purpose

This project contains a number of scripts that help us prepare for upcoming FRC events by leveraging data from The Blue
Alliance. These scripts include:

- Pull all events for a competition year from The Blue Alliance and cache locally as JSON.
- Pull data for an Event from The Blue Alliance and cache locally as JSON.
- Pull the data from the stored JSON into Excel to provide a rich experience for tracking Scouting sessions.
- Pull the data from the stored JSON to produde a much smaller JavaScript file for use in the ScoutingApp.

<!-- Prerequisites -->
<div id="prerequisites"></div>

## Prerequisites

1. Python 3.12 or greater (to execute these scripts)
2. Microsoft Excel or Libre Office (for using spreadsheets)
3. API Key from [The Blue Alliance](https://www.thebluealliance.com/apidocs/v3).

Additionally, the following Python packages need to be installed using the commands below:

```shell
pip install pandas
pip install requests
pip install load_dotenv
pip install openpyxl
```

<!-- How to Use -->
<div id="how-to-use"></div>

## How to Use

1. Navigate to the `The Blue Alliance` folder. We source data from The Blue Alliance.
2. Navigate to the `Game Years` folder. This is where we store and manage the files for each competition year.
3. Create a fodler for the year, unless the folder already exists. For example, if the year is 2027, create a folder
   `2027`. Pretty simple.
4. Create a folder for the Event for which we want to collect scouting data. Note that the folder should reflect the
   **key** specified by The Blue Alliance.

<!-- Purpose -->
<div id="purpose"></div>

## Scripts

### [fabricate-scouting-data.py](./fabricate-scouting-data.py)

Reads the event key from .env and uses the JSON data in the `tba_data` folder for that key to produce tab delimited and
comma delimted files for testing.

### [tba-fetch-event.py](./tba-fetch-event.py)

Reads the event key and The Blue Alliance API key from .env and calls into The Blue Alliance v3 API to request the
Event, Teams and Matches for that key.

The JSON returned is saved into the `tba_data` folder for examination or later use.

The Blue Alliance API endpoint(s) called:

- https://www.thebluealliance.com/api/v3/event/{event_key}
- https://www.thebluealliance.com/api/v3/event/{event_key}/{teams}
- https://www.thebluealliance.com/api/v3/event/{event_key}/{matches}

### [tba-fetch-events-for-year.py](./tba-fetch-events-for-year.py)

Reads the event key and The Blue Alliance API key from .env and calls into The Blue Alliance v3 API to request all the
events for that year.

The JSON returned is saved into the `tba_data` folder for examination or later use.

The Blue Alliance API endpoint(s) called:

- https://www.thebluealliance.com/api/v3/events/{year}

### [tba-push-into-excel.py](./tba-push-into-excel.py)

Reads the event key from .env and uses that key to read the previously stored JSON data in the `tba_data` folder. The
script reads the event, teams and matches files and transforms that data into the Excel Spreadsheet template
[push-into-excel-template.xlsx](./push-into-excel-template.xlsx)

This spreadsheet will be used to receive match data from the QR Code scanner and presents various sheets for examing the
data.

<!-- Todo -->
<div id="todo"></div>

## Todo

We can use conditional formatting on the Matches sheet to provide quick, visual indicators regarding the state of
uploaded data. Here are the different conditions we want to color-code:

1. Match has not yet been scouted. (white)/default
2. Match was scouted once and the scouted team matches the scheduled team. (light green)
3. Match was scouted once and the scouted team does NOT match the scheduled. team. (orange)
4. Match was scouted more than once. (red)

These color codes would allow Games Management to triage issues with scouting sessions.
