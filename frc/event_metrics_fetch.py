import datetime
import json
from datetime import datetime
from pathlib import Path

# Get the directory of the running script
script_dir = Path(__file__).parent  

# Set the logging format.
def status(message):
    print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: {message}")

# Variables
year = 2025
event_code = "NYRO"


def frc_matches_read(year, event_code):
    file_path = script_dir / f"data/{year}.{event_code}.matches.Qualification.json"
    with open(file_path, "r") as f:
        data = json.load(f)

    results = {}
    for match in data:
        for team in match["teams"]:

            result = {
                "key": f"{match['matchNumber']}.{team['station']}",
                "matchNumber": match["matchNumber"],
                "alliance": team["station"],
                "teamNumber": team["teamNumber"]
            }
            
            results[f"{match['matchNumber']}.{team['station']}"] = result
            
    return results

def frc_scores_read(year, event_code, matches):
    file_path = script_dir / f"data/{year}.{event_code}.results.json"
    with open(file_path, "r") as f:
        data = json.load(f)   

    for result in data["MatchScores"]:
        for alliance in result["alliances"]:

            if(alliance["alliance"] == "Blue"):
                matches[f"{result["matchNumber"]}.Blue1"]["endgame"] = alliance["endGameRobot1"] 
                matches[f"{result["matchNumber"]}.Blue2"]["endgame"] = alliance["endGameRobot2"] 
                matches[f"{result["matchNumber"]}.Blue3"]["endgame"] = alliance["endGameRobot3"] 
            else:
                matches[f"{result["matchNumber"]}.Red1"]["endgame"] = alliance["endGameRobot1"] 
                matches[f"{result["matchNumber"]}.Red2"]["endgame"] = alliance["endGameRobot2"] 
                matches[f"{result["matchNumber"]}.Red3"]["endgame"] = alliance["endGameRobot3"] 

    return matches


matches = frc_matches_read(year, event_code)
results = frc_scores_read(year, event_code, matches)

print(json.dumps(matches, indent=4))

for key in results:
    item = results[key]
    
    print(f"{item['matchNumber']}, {item['alliance']}, {item['teamNumber']}, {item['endgame']}")
    
