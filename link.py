import json
import os

# Path to the JSON file
json_file = "monster_dates.json"

# Load existing data from the JSON file (if any)
monster_dates = {}
if os.path.exists(json_file):
    with open(json_file, "r") as f:
        monster_dates = json.load(f)

# Extract unique dates
unique_dates = set()
for dates in monster_dates.values():
    unique_dates.update(dates)

print("Unique dates in the JSON file:", unique_dates)

# Main loop to add new data
while True:
    i = input("Enter the monster name: ")
    if i == "STOP":
        break

    if i.startswith("DATE"):
        date = i.replace("DATE", "")
    else:
        i = i.capitalize()
        if i in monster_dates:
            monster_dates[i].append(date)
        else:
            monster_dates[i] = [date]

        # Write the updated data to the JSON file after each entry
        with open(json_file, "w") as f:
            json.dump(monster_dates, f, indent=4)

print(f"Data saved to {json_file}")
