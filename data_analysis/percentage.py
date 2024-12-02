import json

# Step 1: Read the JSON file
file_path = r"C:\Users\Samuel\Desktop\Libreface\Json\results.json"
with open(file_path, 'r') as file:
    data = json.load(file)

total_kills = 0
gaze_lost_kills = 0
victim_gaze_lost_kills = 0
non_victim_gaze_lost_kills = 0
total_victim_kills = 0
total_non_victim_kills = 0

for kill in data["KillsInvolvingPlayer"]:
    total_kills += 1
    if kill.get("GazeLostInTenSeconds", False):
        gaze_lost_kills += 1

    if kill["Victim"] != "PLAYER_NAME":
        total_victim_kills += 1
        if kill.get("GazeLostInTenSeconds", False):
            victim_gaze_lost_kills += 1
    else:
        total_non_victim_kills += 1
        if kill.get("GazeLostInTenSeconds", False):
            non_victim_gaze_lost_kills += 1

if total_kills > 0:
    percentage_gaze_lost = (gaze_lost_kills / total_kills) * 100
else:
    percentage_gaze_lost = 0

if total_victim_kills > 0:
    percentage_victim_gaze_lost = (victim_gaze_lost_kills / total_victim_kills) * 100
else:
    percentage_victim_gaze_lost = 0

if total_non_victim_kills > 0:
    percentage_non_victim_gaze_lost = (non_victim_gaze_lost_kills / total_non_victim_kills) * 100
else:
    percentage_non_victim_gaze_lost = 0

# Print the results
print(f"Percentage of kills where GazeLostInTenSeconds is true: {percentage_gaze_lost:.2f}%")
print(f"Percentage of victim kills where GazeLostInTenSeconds is true: {percentage_victim_gaze_lost:.2f}%")
print(f"Percentage of non-victim kills where GazeLostInTenSeconds is true: {percentage_non_victim_gaze_lost:.2f}%")
