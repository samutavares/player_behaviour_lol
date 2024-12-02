import json
import requests
from datetime import datetime, timedelta
import csv

API_KEY = "" # INSERT YOUR API
MATCH_REGION = "americas"
puuid = '' #Insert Your PUUID
MATCH_ID = '' #Insert Your MatchId
GAME_START_TIMESTAMP = 1730427865042  

# Function to get match details
def get_match_details(match_id, region, api_key):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
    headers = {
        'X-Riot-Token': api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()

match_details = get_match_details(MATCH_ID, MATCH_REGION, API_KEY)

participant_info = {}
for participant in match_details['info']['participants']:
    participant_info[participant['puuid']] = {
        'gameName': participant['summonerName'],
        'champion': participant['championName'],
        'participantId': participant['participantId']
    }

participant_id_to_puuid = {info['participantId']: puuid for puuid, info in participant_info.items()}

url = f'https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/{MATCH_ID}/timeline'
headers = {
    'X-Riot-Token': API_KEY
}

response = requests.get(url, headers=headers)
timeline = response.json()

champion_kills = []

game_start_time = datetime.utcfromtimestamp(GAME_START_TIMESTAMP / 1000.0)

for frame in timeline['info']['frames']:
    for event in frame['events']:
        if event['type'] == 'CHAMPION_KILL':
            event_timestamp = event['timestamp']
            event_time = game_start_time + timedelta(milliseconds=event_timestamp)
            
            event_time_brt = event_time - timedelta(hours=3)

            killer_puuid = participant_id_to_puuid.get(event['killerId'], 'Unknown')
            victim_puuid = participant_id_to_puuid.get(event['victimId'], 'Unknown')

            killer_info = participant_info.get(killer_puuid, {'gameName': 'Unknown', 'champion': 'Unknown'})
            victim_info = participant_info.get(victim_puuid, {'gameName': 'Unknown', 'champion': 'Unknown'})

            kill_event = {
                'timestamp': event_time_brt.strftime('%Y-%m-%d %H:%M:%S'),
                'killerGameName': killer_info['gameName'],
                'killerChampion': killer_info['champion'],
                'victimGameName': victim_info['gameName'],
                'victimChampion': victim_info['champion']
            }
            champion_kills.append(kill_event)

gaze_data_file_path = r'C:\Users\Samuel\Downloads\TrackingEye.csv'

gaze_data = []
with open(gaze_data_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['Timestamp'] = float(row['Timestamp'])
        row['GazeLost'] = row['GazeLost'].lower() == 'true'
        gaze_data.append(row)

def check_gaze_lost(kills, gaze_data, player_name):
    results = []
    for kill in kills:
        if kill['killerGameName'] == player_name or kill['victimGameName'] == player_name:
            kill_time = datetime.strptime(kill['timestamp'], '%Y-%m-%d %H:%M:%S')
            start_time = kill_time - timedelta(seconds=10)
            end_time = kill_time + timedelta(seconds=10)
            gaze_lost_events = [
                gaze for gaze in gaze_data
                if start_time.timestamp() <= gaze['Timestamp'] <= end_time.timestamp() and gaze['GazeLost']
            ]
            results.append({
                'kill_time': kill['timestamp'],
                'killer': kill['killerGameName'],
                'victim': kill['victimGameName'],
                'gaze_lost_in_ten_seconds': len(gaze_lost_events) > 0,
                'gaze_lost_events': [
                    {
                        'timestamp': datetime.utcfromtimestamp(gaze['Timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                        'GazeLost': gaze['GazeLost']
                    }
                    for gaze in gaze_lost_events
                ]
            })
    return results

player_name = "Thewizard45"
gaze_lost_results = check_gaze_lost(champion_kills, gaze_data, player_name)

file_path = r'C:\Users\Samuel\Desktop\Libreface\Json\samu\samu.json'
with open(file_path, 'r') as file:
    data = json.load(file)

base_timestamp_str = "2024-10-31 23-26-09"
base_timestamp = datetime.strptime(base_timestamp_str, "%Y-%m-%d %H-%M-%S")

def convert_timestamp(base, offset):
    return base + timedelta(milliseconds=offset)

def round_to_nearest_second(dt):
    return dt.replace(microsecond=0)

def extract_emotions(data, start_time, end_time):
    emotions = []
    first_frame_per_second = {}
    for frame in data["Frames"]:
        frame_timestamp = convert_timestamp(base_timestamp, frame["Timestamp"])
        if start_time <= frame_timestamp <= end_time:
            rounded_timestamp = round_to_nearest_second(frame_timestamp)
            if rounded_timestamp not in first_frame_per_second:
                first_frame_per_second[rounded_timestamp] = frame
    
    for timestamp, frame in sorted(first_frame_per_second.items()):
        for face in frame["Faces"]:
            expression = face.get("Expression", {})
            emotions.append({
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'expression': expression
            })
    return emotions

results = {
    "KillsInvolvingPlayer": []
}

for result in gaze_lost_results:
    kill_time = datetime.strptime(result['kill_time'], '%Y-%m-%d %H:%M:%S')
    kill_entry = {
        "KillTime": result['kill_time'],
        "Killer": result['killer'],
        "Victim": result['victim'],
        "Result": "Thewizard45 defeated someone." if result['killer'] == player_name else "Thewizard45 was defeated.",
        "GazeLostInTenSeconds": result['gaze_lost_in_ten_seconds'],
        "EmotionsDuringKill": [],
        "GazeLostEvents": []
    }
    
    kill_emotions = extract_emotions(data, kill_time - timedelta(seconds=10), kill_time + timedelta(seconds=10))
    for emotion in kill_emotions:
        kill_entry["EmotionsDuringKill"].append({
            "Timestamp": emotion['timestamp'],
            "Expression": emotion['expression']
        })
    
    for event in result['gaze_lost_events']:
        event_time_utc = datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S')
        event_time_brt = event_time_utc - timedelta(hours=3)
        gaze_lost_entry = {
            "GazeLostAt": event_time_brt.strftime('%Y-%m-%d %H:%M:%S'),
            "EmotionsDuringGazeLost": []
        }
        
        gaze_lost_time = event_time_brt
        gaze_emotions = extract_emotions(data, gaze_lost_time - timedelta(seconds=10), gaze_lost_time + timedelta(seconds=10))
        for emotion in gaze_emotions:
            gaze_lost_entry["EmotionsDuringGazeLost"].append({
                "Timestamp": emotion['timestamp'],
                "Expression": emotion['expression']
            })
        
        kill_entry["GazeLostEvents"].append(gaze_lost_entry)
    
    results["KillsInvolvingPlayer"].append(kill_entry)

output_file_path = r'C:\\Users\\Samuel\\Desktop\\Libreface\\Json\\results_samu.json'
with open(output_file_path, 'w') as outfile:
    json.dump(results, outfile, indent=4)

print(f"Results saved to {output_file_path}")
