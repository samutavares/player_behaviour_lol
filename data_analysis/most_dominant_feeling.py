import json
import pandas as pd

file_path = 'C:\\Users\\Samuel\\Desktop\\Libreface\\Json\\results_samu.json'
with open(file_path, 'r') as file:
    data = json.load(file)

def find_dominant_emotion(expression):
    return max(expression, key=expression.get), expression[max(expression, key=expression.get)]

results = []

for event in data["KillsInvolvingPlayer"]:
    kill_time = event["KillTime"]
    killer = event["Killer"]
    victim = event["Victim"]
    
    emotions = event["EmotionsDuringKill"]
    if len(emotions) < 2:
        continue
    
    before_kill_killer = find_dominant_emotion(emotions[-2]["Expression"])
    after_kill_killer = find_dominant_emotion(emotions[-1]["Expression"])
    
    results.append({
        "KillTime": kill_time,
        "Role": "Killer",
        "Player": killer,
        "BeforeEmotion": before_kill_killer[0],
        "BeforeValue": before_kill_killer[1],
        "AfterEmotion": after_kill_killer[0],
        "AfterValue": after_kill_killer[1],
    })
    
    if len(emotions) > 1:
        before_kill_victim = find_dominant_emotion(emotions[0]["Expression"])
        after_kill_victim = find_dominant_emotion(emotions[-1]["Expression"])
        results.append({
            "KillTime": kill_time,
            "Role": "Victim",
            "Player": victim,
            "BeforeEmotion": before_kill_victim[0],
            "BeforeValue": before_kill_victim[1],
            "AfterEmotion": after_kill_victim[0],
            "AfterValue": after_kill_victim[1],
        })

df = pd.DataFrame(results)

standard_emotion = (
    df.groupby(["Role", "BeforeEmotion"])["BeforeValue"]
    .mean()
    .reset_index()
    .sort_values(by=["Role", "BeforeValue"], ascending=[True, False])
)


filtered_df = df[df["Player"] == "Thewizard45"]

standard_emotion_filtered = (
    filtered_df.groupby(["Role", "BeforeEmotion"])["BeforeValue"]
    .mean()
    .reset_index()
    .sort_values(by=["Role", "BeforeValue"], ascending=[True, False])
)

print(filtered_df)
print(standard_emotion_filtered)