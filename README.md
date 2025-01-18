# Calling The Blue Alliance API and Pushing into Excel Spreadsheets

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#tba">Purpose</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#scripts">Scripts</a></li>
    <li><a href="#todo">Todo</a></li>
  </ol>
</details>

<!-- Purpose -->
<div id="purpose"></div>

## Purpose

We can create a process where we:

1. Pull data for an Event from The Blue Alliance and cache locally as JSON.
2. Pull the data from the stored JSON into Excel to provide a rich experience
   for tracking Scouting sessions.

<div id="prerequisites"></div>
<!-- Prerequisites -->

## Prerequisites

1. Python 3.12 or greater
2. Microsoft Excel
3. Configure .env to speficy The Blue Alliance API key and other lookups.

Additionally, the following Python packages need to be installed using the
commands below:

```shell
pip install pandas
pip install requests
pip install load_dotenv
pip install openpyxl
```

<!-- Purpose -->
<div id="purpose"></div>

## Scripts

### [fabricate-scouting-data.py](./fabricate-scouting-data.py)

Reads the event key from .env and uses the JSON data in the `tba_data` folder
for that key to produce tab delimited and comma delimted files for testing.

### [fetch-event-from-tba.py](./fetch-event-from-tba.py)

Reads the event key and The Blue Alliance API key from .env and calls into The
Blue Alliance v3 API to request the Event, Teams and Matches for that key.

The JSON returned is saved into the `tba_data` folder for examination or later
use.

The Blue Alliance API endpoint(s) called:

- https://www.thebluealliance.com/api/v3/event/{event_key}
- https://www.thebluealliance.com/api/v3/event/{event_key}/{teams}
- https://www.thebluealliance.com/api/v3/event/{event_key}/{matches}

### [fetch-events-for-year.py](./fetch-events-for-year.py)

Reads the event key and The Blue Alliance API key from .env and calls into The
Blue Alliance v3 API to request all the events for that year.

The JSON returned is saved into the `tba_data` folder for examination or later
use.

The Blue Alliance API endpoint(s) called:

- https://www.thebluealliance.com/api/v3/events/{year}

### [push-into-excel.py](./push-into-excel.py)

Reads the event key from .env and uses that key to read the previously stored
JSON data in the `tba_data` folder. The script reads the event, teams and
matches files and transforms that data into the Excel Spreadsheet template
[push-into-excel-template.xlsx](./push-into-excel-template.xlsx)

This spreadsheet will be used to receive match data from the QR Code scanner and
presents various sheets for examing the data.

<!-- Todo -->
<div id="todo"></div>

## Todo

We can use conditional formatting on the Matches sheet to provide quick, visual
indicators regarding the state of uploaded data. Here are the different
conditions we want to color-code:

1. Match has not yet been scouted. (white)/default
2. Match was scouted once and the scouted team matches the scheduled team.
   (light green)
3. Match was scouted once and the scouted team does NOT match the scheduled.
   team. (orange)
4. Match was scouted more than once. (red)

These color codes would allow Games Management to triage issues with scouting
sessions.
