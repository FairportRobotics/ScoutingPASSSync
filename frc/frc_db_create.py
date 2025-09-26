import sqlite3
import datetime
from datetime import datetime
from pathlib import Path

# Get the directory of the running script
script_dir = Path(__file__).parent  
file_path = script_dir / "frc.db"

connection = sqlite3.connect(file_path)
cursor = connection.cursor()

# Enable foreign key constraints
connection.execute('PRAGMA foreign_keys = ON;')

# Set the logging format.
def status(message):
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: {message}")


def drop_all_tables():
   status("Drop all tables")

   command = """
      DROP TABLE IF EXISTS frc_match_results;
      DROP TABLE IF EXISTS frc_match_teams;
      DROP TABLE IF EXISTS frc_matches;
      DROP TABLE IF EXISTS frc_teams;
      DROP TABLE IF EXISTS frc_events;
   """

   cursor.executescript(command)         

def frc_events_create():
   status("Creating table: frc_events")

   command = """
      CREATE TABLE frc_events (
      key TEXT PRIMARY KEY,
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


def frc_teams_create():
    status("Creating table: frc_teams")

    command = """
    CREATE TABLE frc_teams (
        teamNumber INTEGER PRIMARY KEY,
        nameShort TEXT COLLATE NOCASE NOT NULL,
        nameFull TEXT COLLATE NOCASE NOT NULL,
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


def frc_matches_create():
    status("Creating table: frc_matches")

    command = """
    CREATE TABLE frc_matches (
        key TEXT PRIMARY KEY,
        eventKey TEXT COLLATE NOCASE NOT NULL,
        year INTEGER NOT NULL,
        code TEXT COLLATE NOCASE NOT NULL,
        tournamentLevel TEXT COLLATE NOCASE NOT NULL,
        matchNumber INTEGER NOT NULL,
        startTime TEXT,
        description TEXT COLLATE NOCASE,
        field TEXT COLLATE NOCASE,

        FOREIGN KEY(eventKey) REFERENCES frc_events(key)
    );
    """

    cursor.executescript(command) 


def frc_match_teams_create():
    status("Creating table: frc_match_teams")

    command = """
    CREATE TABLE frc_match_teams (
        matchKey TEXT COLLATE NOCASE NOT NULL,
        station INTEGER NOT NULL,
        alliance TEXT COLLATE NOCASE NOT NULL,
        number INTEGER NOT NULL,
        teamNumber INTEGER NOT NULL,
        surrogate BOOLEAN NOT NULL,

        FOREIGN KEY(matchKey) REFERENCES frc_matches(key),
        FOREIGN KEY(teamNumber) REFERENCES frc_teams(teamNumber)
    );
    """

    cursor.executescript(command) 


def frc_match_results_create():
   status("Creating table: frc_match_results")

   command = """
   DROP TABLE IF EXISTS frc_match_results;

   CREATE TABLE frc_match_results (
      matchKey TEXT PRIMARY KEY,
      winningAlliance TEXT COLLATE NOCASE NOT NULL,
      coopertitionBonusAchieved BOOLEAN,
      coralBonusLevelsThresholdCoop INTEGER NOT NULL,
      coralBonusLevelsThresholdNonCoop INTEGER NOT NULL,
      coralBonusLevelsThreshold INTEGER NOT NULL,
      bargeBonusThreshold INTEGER NOT NULL,
      autoBonusCoralThreshold INTEGER NOT NULL,
      autoBonusRobotsThreshold INTEGER NOT NULL,

      FOREIGN KEY(matchKey) REFERENCES frc_matches(key)
   );
   """

   cursor.executescript(command)


def frc_match_results_alliance_create():
   status("Creating table: frc_match_results_alliance")

   command = """
   CREATE TABLE frc_match_results_alliance (
      matchKey TEXT PRIMARY KEY,
      alliance TEXT COLLATE NOCASE NOT NULL, 

      
      winningAlliance TEXT COLLATE NOCASE NOT NULL,
      coopertitionBonusAchieved BOOLEAN,
      coralBonusLevelsThresholdCoop INTEGER NOT NULL,
      coralBonusLevelsThresholdNonCoop INTEGER NOT NULL,
      coralBonusLevelsThreshold INTEGER NOT NULL,
      bargeBonusThreshold INTEGER NOT NULL,
      autoBonusCoralThreshold INTEGER NOT NULL,
      autoBonusRobotsThreshold INTEGER NOT NULL,

      FOREIGN KEY(matchKey) REFERENCES frc_matches(key)
   );
   """

   cursor.executescript(command)     

# Create the tables.
drop_all_tables()
frc_events_create()
frc_teams_create()
frc_matches_create()
frc_match_teams_create()
frc_match_results_create()
