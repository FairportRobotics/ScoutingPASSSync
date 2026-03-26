# Scouting Data Support

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#tba">Purpose</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#scripts">Scripts</a></li>
    <li><a href="#prepare-environment">Prepare Environment</a></li>
    <li><a href="#initialize-competition-year">Initialize Competition Year</a></li>
    <li><a href="#initialize-competition-event">Initialize Competition Event</a></li>
    <li><a href="#prepare-competition-event">Prepare Competition Event</a></li>
    <li><a href="#how-to">How To</a></li>
  </ol>
</details>

<!-- Purpose -->
<div id="purpose"></div>

## Purpose

This project contains a number of scripts that help us prepare for upcoming FRC events by leveraging data from The Blue
Alliance. These scripts include:

- Pull all events for a competition year from The Blue Alliance and cache locally as JSON.
- Pull data for an Event from The Blue Alliance and cache locally as JSON.
- Pull the data from the stored Event JSON into Excel to provide a rich experience for tracking Scouting sessions.
- Pull the data from the stored Event JSON to produde a much smaller JavaScript file for use in the ScoutingApp.

<!-- Prerequisites -->
<div id="prerequisites"></div>

## Prerequisites

1. Python 3.12 or greater (to execute these scripts)
2. Microsoft Excel or Libre Office (for using spreadsheets)
3. API Key from [The Blue Alliance](https://www.thebluealliance.com/apidocs/v3). (Refer to <a href="#how-to">How To</a>
   for instructions)

The required Python packages can be installed by executing the command below:

```shell
pip install -r requirements.txt
```

Alternatively, you can install needed packages manually:

```shell
pip install pandas
pip install requests
pip install load_dotenv
pip install openpyxl
```

<!-- Scripts -->
<div id="scripts"></div>

| File                       | Description                                                                                                                                                                                                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| event_initialize.py        | AAA                                                                                                                                                                                                                                                                             |
| event_push_to_excel.py     | BBB                                                                                                                                                                                                                                                                             |
| event_to_scouting_app.py   | CCC                                                                                                                                                                                                                                                                             |
| fabricate_scouting_data.py | Generates bogus and random data (comma delimited and tab delimited) and writes to<br> `The Blue Alliance\Game Years\TBA_EVENT_YEAR\TBA_EVENT_KEY\TBA_EVENT_KEY.fake-data.csv`<br>and<br>`The Blue Alliance\Game Years\TBA_EVENT_YEAR\TBA_EVENT_KEY\TBA_EVENT_KEY.fake-data.tsv` |
| year_initialize.py         | Downloads all the currently registered events for a Competition year and writes the JSON to<br> `The Blue Alliance\Game Years\TBA_EVENT_YEAR\TBA_EVENT_KEY\TBA_EVENT_KEY.json`                                                                                                  |

---

<!-- How to Use -->
<div id="prepare-environment"></div>

## Prepare environment

Create or validate the existence of the file `The Blue Alliance\.env`. This is a simple file which is used to store
settings and secrets or use by the scripts. This file is included in the `.gitignore` as we do not want the file to be
added to source control.

The conents of the file should follow what you see in `.env.example` and currently looks something like:

```text
TBA_AUTH_KEY="blue-alliance-api-key"
TBA_EVENT_YEAR="2026"
TBA_EVENT_KEY="2026abcde"
```

**TBA_AUTH_KEY** is the TBA key acquired from
[The Blue Alliance Accounts Page](https://www.thebluealliance.com/account). **TBA_EVENT_YEAR** is the FRC competition
year for which we want to manage scouting data. **TBA_EVENT_KEY** will be explained later.

<!-- Initialize Competition Year -->
<div id="initialize-competition-year"></div>

## Initialize Competition Year

Once you have set `TBA_AUTH_KEY` and `TBA_EVENT_YEAR`, open the file `year_initialize.py` and execute it.

This script queries the TBA API, provides the authorization key and the desired year, and receives the list of events
for the year.

The script then creates a folder in `The Blue Alliance\Game Years` for that year and saves the JSON as YEAR.json.

For example, if you wanted to get the data for the year 1234, you would:

1. Update `.env` with `TBA_EVENT_YEAR="1234"`
2. Execute `initialize_year.py`
3. Navigate to `The Blue Alliance\Game Years\1234`.
4. Observe the file `1234.json` exists and contains all the events for that year.

<!-- Initialize a specific Event -->
<div id="initialize-competition-event"></div>

## Initialize Competition Event

To prepare for a specific Event, update `The Blue Alliance\.env` to include the TBA Event key from
`TBA_EVENT_YEAR.json`. Look for the "key" property in that JSON. For example, for **Rocket City Regional**, the key is
`2026alhu`:

```json
[
  {
    "key": "2026alhu",
    "name": "Rocket City Regional"
    /* Lots more JSON */
  },
  {
    "key": "2026arc",
    "name": "Archimedes Division"
    /* Lots more JSON */
  },
  {
    "key": "2026nyro",
    "name": "Finger Lakes Regional"
    /* Lots more JSON */
  }
  /* Lots more JSON */
]
```

For example, if you wanted to get the data for the **Rocket City Regional**, you would:

1. Update `.env` with `TBA_EVENT_KEY="2026alhu"`
2. Execute `event_initialize.py`
3. Navigate to `The Blue Alliance\Game Years\2026\2026alhu`.
4. Observe the folder contains data related to the event:
   - 2026alhu.json
   - 2026alhu.matches.json
   - 2026alhu.teams.json

The files and scripts related to the Event are as follows:

| File                   | Description                                                                                                                                                                                                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EVENT_KEY.json         | This file contains meta data about the event itself. This is roughly the same information as you would find in `The Blue Alliance\Game Years\2026.json`.                                                                          |
| EVENT_KEY.matches.json | This file contains all the known information about the matches designated for the Event. Note that this file might not be populated. Typically, TBA will publish the final Match data the day before or the morning of the Event. |
| EVENT_KEY.teams.json   | This file contains all the known information about the Teams competing at the Event. Note that this file might not be populated. TBA updates this data long before the Event takes place.                                         |
|                        |

---

<!-- Prepare for the Event -->
<div id="prepare-competition-event"></div>

## Prepare for the Event

Now that we have initialized an Event, we can start to prepare the Excel spreadsheet for receiving and reporting on
Scouting data.

<!-- How To -->
<div id="how-to"></div>

## How To

### Obtain Blue Alliance API Key

1. Navigate to [The Blue Alliance](https://www.thebluealliance.com/)
2. Click **myTBA**
3. FOllow the instructions to either create a new account or log into an existing account.
4. Scroll down to the **Read API Keys** section.
5. Enter a value for **Description**
6. Click **Add New Key**
7. Copy the **X-TBA-Auth-Key** value into `.env` files where desired.

### Prepare for a new competition year

1. Work with members working on the ScoutingPASS and update the **MatchScoutingData** tab in the
   `The Blue Alliance\Templates\tba_push_into_excel_template.xlsx` spreadsheet.
2. Work with members working on the ScoutingPASS and update the script
   `The Blue Alliance\Templates\tba_push_into_excel.py` to account for how we want to consume and report on scouting
   data.
3. Follow the guidance in <a href="#initialize-competition-year">Initialize Competition Year</a>

### Prepare for a new competition event

TBD

### Adjust scouting data beteween events

TBD
