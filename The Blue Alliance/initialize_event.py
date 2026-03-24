from datetime import datetime
import json
import os
import requests
import shutil
import pandas as pd
from dotenv import load_dotenv 

# Load the .env file and all environment variables.
load_dotenv()

# Define the status function.
def status(message):
    print(f"{datetime.now()}: {message}")

# Retrieve values from .env.
tbaAuthKey = os.getenv("TBA_AUTH_KEY")
tbaAuthHeader =  {"X-TBA-Auth-Key": tbaAuthKey}
if tbaAuthKey is None:
    raise ValueError("TBA_AUTH_KEY is not set")

tbaEventYear = os.getenv("TBA_EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("TBA_EVENT_YEAR is not set")

tbaEventKey = os.getenv("TBA_EVENT_KEY")
if tbaEventKey is None:
    raise ValueError("TBA_EVENT_KEY is not set")


# Validate arguments.
if tbaEventYear == "":
    status("No event year provided.")
    exit()

if tbaAuthKey == "":
    status("No TBA Auth key provided.")
    exit()         


# Define folder paths.
current_directory = os.path.dirname(os.path.abspath(__file__))
target_year_directory = os.path.join(current_directory, "Game Years", tbaEventYear)
target_event_directory = os.path.join(current_directory, "Game Years", tbaEventYear, tbaEventKey)
template_directory = os.path.join(current_directory, "Templates")
os.makedirs(target_event_directory, exist_ok=True)


def fetch_event():
    # Prepare the API call.
    status(f"Fetching Event...")
    eventUrl = f"https://www.thebluealliance.com/api/v3/event/{tbaEventKey}"
    tbaEvent = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaEvent = json.loads(tbaEvent.text)

    # Emit a status message based on results of the API call.
    if("Error" in tbaEvent):
        status(f"Fetching Event: '{tbaEventKey}' was not returned")
    else:
        status(f"Fetching Event: '{tbaEvent["short_name"]}'")

    # Log to file.
    filePath = os.path.join(target_event_directory, f"{tbaEventKey}.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaEvent, f, indent=3)

    return tbaEvent

def fetch_teams():
    # Prepare the API call.
    status(f"Fetching Teams...")
    eventUrl = f"https://www.thebluealliance.com/api/v3/event/{tbaEventKey}/teams"
    response = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaTeams = json.loads(response.text)

    # Emit a status message based on results of the API call.
    if("Error" in tbaTeams):
        status(f"Fetching Teams: 0 Teams")
    else:
        status(f"Fetching Teams: {len(tbaTeams)} Teams")    

    # Log to file.
    filePath = os.path.join(target_event_directory, f"{tbaEventKey}.teams.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaTeams, f, indent=3)    

    return tbaTeams

def fetch_matches():
    # Prepare the API call.
    status(f"Fetching Matches...")
    eventUrl = f"https://www.thebluealliance.com/api/v3/event/{tbaEventKey}/matches"
    tbaMatches = requests.get(eventUrl, headers=tbaAuthHeader)
    tbaMatches = json.loads(tbaMatches.text)

    # Emit a status message based on results of the API call.
    if("Error" in tbaMatches):
        status(f"Fetching Matches: 0 Matches")
    else:
        status(f"Fetching Matches: {len(tbaMatches)} Matches")      

    # Log to file.
    filePath = os.path.join(target_event_directory, f"{tbaEventKey}.matches.json")
    with open(filePath, 'w', newline='') as f:
        json.dump(tbaMatches, f, indent=3)

    return tbaMatches

def copy_excel_template():
    # Prepare the API call.
    source_file = "tba_push_into_excel_template.xlsx"    
    source = os.path.join(template_directory, source_file)
    dest = os.path.join(target_event_directory, source_file)

    status(f"Copying {source_file}...")
    if os.path.exists(dest):
        status(f"WARNING: Skipping {source_file} (exists at destination)")
        status(f"WARNING: delete {source_file} and run again to copy")
        return
    
    try:
        shutil.copy2(source, dest)
    except:
        status("ERROR: Unable to copy")

def copy_excel_populate_script():
    # Prepare the API call.
    source_file = "tba_push_into_excel.py"
    source = os.path.join(template_directory, source_file)
    dest = os.path.join(target_event_directory, source_file)

    status(f"Copying {source_file}...")
    if os.path.exists(dest):
        status(f"WARNING: Skipping {source_file} (exists at destination)")
        status(f"WARNING: delete {source_file} and run again to copy")
        return
    
    try:
        shutil.copy2(source, dest)
    except:
        status("ERROR: Unable to copy")

def copy_fabricate_data_script():
    # Prepare the API call.
    source_file = "fabricate-scouting-data.py"
    source = os.path.join(template_directory, source_file)
    dest = os.path.join(target_event_directory, source_file)

    status(f"Copying {source_file}...")
    if os.path.exists(dest):
        status(f"WARNING: Skipping {source_file} (exists at destination)")
        status(f"WARNING: delete {source_file} and run again to copy")
        return
    
    try:
        shutil.copy2(source, dest)
    except:
        status("ERROR: Unable to copy")

def copy_create_scouting_app_match_javascript():
    # Prepare the API call.
    source_file = "tba_push_for_app.py"
    source = os.path.join(template_directory, source_file)
    dest = os.path.join(target_event_directory, source_file)

    status(f"Copying {source_file}...")
    if os.path.exists(dest):
        status(f"WARNING: Skipping {source_file} (exists at destination)")
        status(f"WARNING: delete {source_file} and run again to copy")
        return
    
    try:
        shutil.copy2(source, dest)
    except:
        status("ERROR: Unable to copy") 


fetch_event()
fetch_teams()
fetch_matches()

copy_excel_template()
copy_excel_populate_script()
copy_fabricate_data_script()
copy_create_scouting_app_match_javascript()