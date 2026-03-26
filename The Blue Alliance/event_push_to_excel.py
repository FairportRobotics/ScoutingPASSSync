import json
import os
import json
import os

from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule, ColorScaleRule
from dotenv import load_dotenv 

# Define the status message function.
def status(message):
    print(f"{datetime.now()}: {message}")


# Load the .env file and all environment variables.
load_dotenv()

# Retrieve values from .env.
tbaEventYear = os.getenv("TBA_EVENT_YEAR")
if tbaEventYear is None:
    raise ValueError("TBA_EVENT_YEAR is not set")

tbaEventKey = os.getenv("TBA_EVENT_KEY")
if tbaEventKey is None:
    raise ValueError("TBA_EVENT_KEY is not set")

status(f"Processing {tbaEventKey}")


# Define folder paths.
current_directory = os.path.dirname(os.path.abspath(__file__))
target_event_directory = os.path.join(current_directory, "Game Years", tbaEventYear, tbaEventKey)
template_directory = os.path.join(current_directory, "Templates")
os.makedirs(target_event_directory, exist_ok=True)


# Set various variables we can use throughout the script.
template_file_name = os.path.join(template_directory, "scouting_template.xlsx")
ouput_file_name = os.path.join(target_event_directory, f"{tbaEventKey}.xlsx")


# Set constants we can use.
font_header    = Font(bold=True,  size=12, color="FFFFFF")
font_data      = Font(bold=False, size=12, color="000000")

align_center   = Alignment(horizontal="center", vertical="center")
align_vertical = Alignment(horizontal="left",   vertical="bottom", text_rotation=90) 

fill_default   = PatternFill(start_color="595959", end_color="595959", fill_type="solid") 
fill_blue      = PatternFill(start_color="2471A3", end_color="2471A3", fill_type="solid")   
fill_red       = PatternFill(start_color="CB4335", end_color="CB4335", fill_type="solid")   
fill_green     = PatternFill(start_color="229954", end_color="229954", fill_type="solid")   
fill_orange    = PatternFill(start_color="D68910", end_color="D68910", fill_type="solid")  

color_scale_rule = ColorScaleRule(
    start_type="min", start_color="CB4335",                     # Red for minimum value
    mid_type="percentile", mid_value=50, mid_color="D68910",    # Yellow for mid value
    end_type="max", end_color="229954"                          # Green for maximum value
)

format_comma = '#,##0;-[Red]#,##0;"-"'
format_percent = '0.0%'


# Load the workbook and save it as the destination workbook.
status(f"Preparing the spreadsheet: {ouput_file_name}")
wb = load_workbook(template_file_name)
wb.save(ouput_file_name)

# Workaround for the inability to do something like this:
# row[counter += 1]
def incrementer(start):
    while True:
        start += 1
        yield start


# Define the function that can freeze panes and set auto filter.
def apply_view(ws, freeze_range, auto_filter_range):

    if not freeze_range is None:
        ws.freeze_panes =freeze_range

    if not auto_filter_range is None:
        ws.auto_filter.ref = auto_filter_range     


# Accepts a sheet and a list of format definitions and applies them to the sheet.
# This allows us to apply a variable number of formats to cell ranges.
def apply_formats(ws, formats):
    for format in formats:
        # Extract the range definition and the formats to apply.
        range = format["range"]
        fill = format.get("fill")
        font = format.get("font")
        alignment = format.get("alignment")
        number_format = format.get("number_format")

        # Enumerate over the cells in the range.
        for cell_row in ws[range]:

            # Apply formats to each individual cell.
            for cell in cell_row:
                if not fill is None:
                    cell.fill = fill
                if not font is None:
                    cell.font = font
                if not alignment is None:
                    cell.alignment = alignment
                if not number_format is None:
                    cell.number_format = number_format


# Define the the function that reads and pushes the Event.
def prepate_sheet_event():
    status("Pushing Event data...")

    # Read the JSON data from the file.
    with open(os.path.join(target_event_directory, f"{tbaEventKey}.json"), "r") as f:
        data = json.load(f)

    # Load the Event sheet.
    ws = wb["Event"]

    # Write the Event data to the sheet.
    ws["B1"] = data["key"]
    ws["B2"] = data["event_code"]
    ws["B3"] = data["name"]
    ws["B4"] = data["location_name"]
    ws["B5"] = data["start_date"]

    # Apply formatting to the sheet.
    apply_formats(ws, [
        { "range": f"B1:B5", "font": font_data },
    ])


# Define the the function that reads and pushes the Teams.
def prepare_sheet_teams():
    status("Pushing Team data...")

    # Read the JSON data from the file.
    with open(os.path.join(target_event_directory, f"{tbaEventKey}.teams.json"), "r") as f:
        data = json.load(f)
        data = sorted(data, key=lambda x: x["team_number"])

    # Load the Teams sheet.
    ws = wb["Teams"]

    # Write the data to the sheet.
    for index, row in enumerate(data):
        row_num = index + 2
        ws.cell(row=row_num, column=1, value=row["team_number"])
        ws.cell(row=row_num, column=2, value=row["nickname"])
        ws.cell(row=row_num, column=3, value=row["school_name"])
        ws.cell(row=row_num, column=4, value=row["rookie_year"])
        ws.cell(row=row_num, column=5, value=row["key"])
  
    # Apply formatting to the sheet.
    apply_formats(ws, [
        { "range": f"A2:A{str(len(data) + 1)}", "font": font_data },
    ])


# Define the the function that reads and pushes the Matches.
def prepare_sheet_matches():
    status("Pushing Match data...")

    # Set the conditional formatting rules.
    fill_scouted = PatternFill(start_color="C8D6A1", end_color="C8D6A1", fill_type="solid")
    fill_duplicate_match = PatternFill(start_color="FFFF54", end_color="FFFF54", fill_type="solid")
    fill_wrong_team = PatternFill(start_color="F5C242", end_color="F5C242", fill_type="solid")

    # Read the JSON data from the file.
    with open(os.path.join(target_event_directory, f"{tbaEventKey}.matches.json"), "r") as f:
        data = json.load(f)
        data = [row for row in data if row["comp_level"] == "qm"]
        data = sorted(data, key=lambda x: x["match_number"])

    # Load the Teams sheet.
    ws = wb["Matches"]

    # Write the data to the sheet.
    for index, row in enumerate(data):
        row_num = index + 2
        ws.cell(row=row_num, column=1, value=row["match_number"])
        ws.cell(row=row_num, column=2, value=datetime.fromtimestamp(row["time"]).strftime("%Y-%m-%d %H:%M:%S"))
        ws.cell(row=row_num, column=3, value=int(row["alliances"]["blue"]["team_keys"][0].replace("frc", "")))
        ws.cell(row=row_num, column=4, value=int(row["alliances"]["blue"]["team_keys"][1].replace("frc", "")))
        ws.cell(row=row_num, column=5, value=int(row["alliances"]["blue"]["team_keys"][2].replace("frc", "")))
        ws.cell(row=row_num, column=6, value=int(row["alliances"]["red"]["team_keys"][0].replace("frc", "")))
        ws.cell(row=row_num, column=7, value=int(row["alliances"]["red"]["team_keys"][1].replace("frc", "")))
        ws.cell(row=row_num, column=8, value=int(row["alliances"]["red"]["team_keys"][2].replace("frc", "")))

        # Add conditional formatting that cannot be applied to a range.
        for col in ["C", "D", "E", "F", "G", "H"]:
            scouted_wrong_team = FormulaRule(formula=[f"=IF(VLOOKUP(CONCATENATE($A{row_num}, \".\", ${col}$1),MatchScoutingData!$A$2:$E$1000, 5, FALSE) = ${col}{row_num}, FALSE, TRUE)"], fill=fill_wrong_team)
            ws.conditional_formatting.add(f"{col}{row_num}", scouted_wrong_team)

  
    # Apply formatting to the sheet.
    apply_formats(ws, [
        { "range": f"A1:B1", "font": font_header ,"fill": fill_default, "alignment": align_center },
        { "range": f"C1:E1", "font": font_header ,"fill": fill_blue, "alignment": align_center },
        { "range": f"F1:H1", "font": font_header ,"fill": fill_red, "alignment": align_center },
        { "range": f"A2:H{str(len(data) + 1)}", "font": font_data, "alignment": align_center },
    ])

    # Add conditional formatting rules that can be applied to a range.
    # =COUNTIF(Where do you want to look?, What do you want to look for?)
    rule_scouted = FormulaRule(formula=["=COUNTIF(MatchScoutingData!$A$2:$A$1000, CONCATENATE($A2,\".\",C$1)) = 1"], fill=fill_scouted)
    rule_scouted_multiple = FormulaRule(formula=["=COUNTIF(MatchScoutingData!$A$2:$A$1000, CONCATENATE($A2,\".\",C$1)) > 1"], fill=fill_duplicate_match)
    ws.conditional_formatting.add("C2:H1000", rule_scouted)
    ws.conditional_formatting.add("C2:H1000", rule_scouted_multiple)

    # Provide a key so it is wasy to understand conditional formatting.
    ws[f"J2"] = "Match has not yet been scouted"
    ws[f"J3"] = "Match has been scouted"
    ws[f"J4"] = "Match was scouted more than once"
    ws[f"J5"] = "Wrong team was scouted"

    # Apply formats to the key.
    apply_formats(ws, [
        { "range": f"J3:J3", "fill": fill_scouted },
        { "range": f"J4:J4", "fill": fill_duplicate_match },
        { "range": f"J5:J5", "fill": fill_wrong_team  },
    ])    


# Deine the function that prepares the Team Scores sheet.
def prepare_sheet_team_scores():
    status("Prepating Team Scores sheet...")

    # Read the JSON data from the file.
    with open(os.path.join(target_event_directory, f"{tbaEventKey}.teams.json"), "r") as f:
        data = json.load(f)
        data = sorted(data, key=lambda x: x["team_number"])

    # Capture the extents of the sheet and data.
    start_row = 3
    record_count = len(data)
    end_row = start_row + record_count - 1

    # Open the Teams sheet.
    ws = wb["Team Scores"]

    # Write the team numbers to the sheet.
    for index, row in enumerate(data):
        row_num = index + start_row
        ws.cell(row=row_num, column=1, value=row["team_number"])  

    # Apply the formulas.
    for row in range(start_row, start_row + record_count):
        # General
        ws[f"B{row}"] = f"=COUNTIF(MatchScoutingData!E$2:E$1000, $A{row})"                                  # Matches Scouted

        # Auto
        ws[f"C{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!F$2:F$1000)"    # Climbed
        ws[f"D{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!G$2:G$1000)"    # Level 1
        ws[f"E{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!H$2:H$1000)"    # Moved
        ws[f"F{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!I$2:I$1000)"    # A-Stop
        ws[f"G{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!J$2:J$1000)"    # Fuel Score

        # Teleop
        ws[f"H{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!K$2:K$1000)"    # Shooting Speed
        ws[f"I{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!L$2:L$1000)"    # Accuracy
        ws[f"J{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!M$2:M$1000)"    # Fuel Collected
        ws[f"K{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!N$2:N$1000)"    # Collect Inactive
        ws[f"L{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!O$2:O$1000)"    # Did Pass
        ws[f"M{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!P$2:P$1000)"    # Collect Alliance Zone
        ws[f"N{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!Q$2:Q$1000)"    # Collect Neutral Zone
        ws[f"O{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!R$2:R$1000)"    # Was Intake Good

        # Endgame        
        ws[f"P{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!S$2:S$1000)"    # Climb Success
        ws[f"Q{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!T$2:T$1000)"    # Defense Whole Game
        ws[f"R{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!U$2:U$1000)"    # Shot from Same Position
        ws[f"S{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!V$2:V$1000)"    # Shoot to End
        ws[f"T{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!W$2:W$1000)"    # Performance
        ws[f"U{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!X$2:X$1000)"    # Result
        ws[f"V{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!AB$2:AB$1000)"  # Total Points

        # Ranking Points
        ws[f"W{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!Y$2:Y$1000)"    # Energized Ranking Point
        ws[f"X{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!Z$2:Z$1000)"    # Supercharged Ranking Point
        ws[f"Y{row}"] = f"=SUMIF(MatchScoutingData!$E$2:$E$1000, $A{row}, MatchScoutingData!AA$2:AA$1000)"  # Traversal Ranking Point
        ws[f"Z{row}"] = f"=SUM(W{row}:Y{row})"                                                              # Total Ranking Points

  
    # Apply formatting to the sheet.
    apply_formats(ws, [
        # Team / Scouted Count
        { "range": f"A{start_row}:B{end_row}", "font": font_header, "fill": fill_default },

        # Format the data cells.
        { "range": f"C{start_row}:Z{end_row}", "font": font_data, "number_format": format_comma },        
    ])


# Define the function that prepares the Team Summary sheet.
def prepare_sheet_team_summary():
    status("Prepating Team Summary sheet...")

    # Read the JSON data from the file.
    with open(os.path.join(target_event_directory, f"{tbaEventKey}.teams.json"), "r") as f:
        data = json.load(f)
        data = sorted(data, key=lambda x: x["team_number"])

    # Capture the extents of the sheet and data.
    record_count = len(data)
    start_row = 3
    end_row = start_row + record_count - 1

    # Open the Teams sheet.
    ws = wb["Team Summary"]

    # Write the team numbers to the sheet.
    for index, row in enumerate(data):
        row_num = index + start_row
        ws.cell(row=row_num, column=1, value=row["team_number"])

    # Apply the formulas.
    for row in range(start_row, end_row + 1):

        # General
        ws[f"B{row}"] = f"=COUNTIF(MatchScoutingData!E$2:E$1000, $A{row})"                       # Matches Scouted

        # Auto
        ws[f"C{row}"] = f"=PERCENTRANK('Team Scores'!$C$3:$C$1000, 'Team Scores'!$C{row}, 3)"    # Climbed
        ws[f"D{row}"] = f"=PERCENTRANK('Team Scores'!$D$3:$D$1000, 'Team Scores'!$D{row}, 3)"    # Level 1
        ws[f"E{row}"] = f"=PERCENTRANK('Team Scores'!$E$3:$E$1000, 'Team Scores'!$E{row}, 3)"    # Moved
        ws[f"F{row}"] = f"=PERCENTRANK('Team Scores'!$F$3:$F$1000, 'Team Scores'!$F{row}, 3)"    # A-Stop
        ws[f"G{row}"] = f"=PERCENTRANK('Team Scores'!$G$3:$G$1000, 'Team Scores'!$G{row}, 3)"    # Fuel Score

        # Teleop
        ws[f"H{row}"] = f"=PERCENTRANK('Team Scores'!$H$3:$H$1000, 'Team Scores'!$H{row}, 3)"    # Shooting Speed
        ws[f"I{row}"] = f"=PERCENTRANK('Team Scores'!$I$3:$I$1000, 'Team Scores'!$I{row}, 3)"    # Accuracy
        ws[f"J{row}"] = f"=PERCENTRANK('Team Scores'!$J$3:$J$1000, 'Team Scores'!$J{row}, 3)"    # Fuel Collected
        ws[f"K{row}"] = f"=PERCENTRANK('Team Scores'!$K$3:$K$1000, 'Team Scores'!$K{row}, 3)"    # Collect Inactive
        ws[f"L{row}"] = f"=PERCENTRANK('Team Scores'!$L$3:$L$1000, 'Team Scores'!$L{row}, 3)"    # Did Pass
        ws[f"M{row}"] = f"=PERCENTRANK('Team Scores'!$M$3:$M$1000, 'Team Scores'!$M{row}, 3)"    # Collect Alliance Zone
        ws[f"N{row}"] = f"=PERCENTRANK('Team Scores'!$N$3:$N$1000, 'Team Scores'!$N{row}, 3)"    # Collect Neutral Zone
        ws[f"O{row}"] = f"=PERCENTRANK('Team Scores'!$O$3:$O$1000, 'Team Scores'!$O{row}, 3)"    # Was Intake Good

        # Endgame        
        ws[f"P{row}"] = f"=PERCENTRANK('Team Scores'!$P$3:$P$1000, 'Team Scores'!$P{row}, 3)"    # Climb Success
        ws[f"Q{row}"] = f"=PERCENTRANK('Team Scores'!$Q$3:$Q$1000, 'Team Scores'!$Q{row}, 3)"    # Defense Whole Game
        ws[f"R{row}"] = f"=PERCENTRANK('Team Scores'!$R$3:$R$1000, 'Team Scores'!$R{row}, 3)"    # Shot from Same Position
        ws[f"S{row}"] = f"=PERCENTRANK('Team Scores'!$S$3:$S$1000, 'Team Scores'!$S{row}, 3)"    # Shoot to End
        ws[f"T{row}"] = f"=PERCENTRANK('Team Scores'!$T$3:$T$1000, 'Team Scores'!$T{row}, 3)"    # Performance

        # Ranking Points
        ws[f"U{row}"] = f"=PERCENTRANK('Team Scores'!$U$3:$U$1000, 'Team Scores'!$U{row}, 3)"    # Result
        ws[f"V{row}"] = f"=PERCENTRANK('Team Scores'!$V$3:$V$1000, 'Team Scores'!$V{row}, 3)"    # Total Points
        ws[f"W{row}"] = f"=PERCENTRANK('Team Scores'!$W$3:$W$1000, 'Team Scores'!$W{row}, 3)"    # Energized Ranking Point
        ws[f"X{row}"] = f"=PERCENTRANK('Team Scores'!$X$3:$X$1000, 'Team Scores'!$X{row}, 3)"    # Supercharged Ranking Point
        ws[f"Y{row}"] = f"=PERCENTRANK('Team Scores'!$Y$3:$Y$1000, 'Team Scores'!$Y{row}, 3)"    # Traversal Ranking Point
        ws[f"Z{row}"] = f"=PERCENTRANK('Team Scores'!$Z$3:$Z$1000, 'Team Scores'!$Z{row}, 3)"    # Total Ranking Points

        # Overall
        ws[f"AA{row}"] = f"=AVERAGE(C{row}:G{row})"  
        ws[f"AB{row}"] = f"=AVERAGE(H{row}:O{row})"  
        ws[f"AC{row}"] = f"=AVERAGE(P{row}:T{row})"  
        ws[f"AD{row}"] = f"=AVERAGE(U{row}:X{row})"  
        ws[f"AE{row}"] = f"=AVERAGE(AA{row}:AD{row})"  


    # Apply the formats to the cells.
    apply_formats(ws, [
        # Team / Scouted Count
        { "range": f"A{start_row}:B{end_row}", "font": font_header, "fill": fill_default },

        # All data cells.
        #{ "range": f"B{start_row}:B{end_row}", "number_format": format_comma },
        { "range": f"C{start_row}:AE{end_row}", "number_format": format_percent },
    ])

    # Build and apply the conditional formatting rules to produce a heatmap for percentiles.
    ws.conditional_formatting.add(f"C{start_row}:AE{end_row}", color_scale_rule)


# Push the data into the spreadsheet.
prepate_sheet_event()
prepare_sheet_teams()
prepare_sheet_matches()
prepare_sheet_team_scores()
prepare_sheet_team_summary()

# And finally, save the spreadsheet.
status(f"Saving to {ouput_file_name}...")
wb.save(ouput_file_name)

