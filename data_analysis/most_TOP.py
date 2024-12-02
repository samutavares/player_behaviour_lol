import json

with open(r'C:\Users\Samuel\Desktop\Libreface\Json\results_samu.json') as file:
    data = json.load(file)

def get_dominant_emotion(expression):
    return max(expression, key=expression.get)

for kill_event in data["KillsInvolvingPlayer"]:
    emotions_before = []
    emotions_after = []

    emotions_during_kill = kill_event["EmotionsDuringKill"]

    kill_time_index = None
    for i, emotion_data in enumerate(emotions_during_kill):
        if emotion_data["Timestamp"] == kill_event["KillTime"]:
            kill_time_index = i
            break

    if kill_time_index is not None:
        emotions_before = emotions_during_kill[:kill_time_index]
        emotions_after = emotions_during_kill[kill_time_index + 1:]

    if emotions_before:
        dominant_emotion_before = get_dominant_emotion(emotions_before[-1]["Expression"])
        kill_event["DominantEmotionBeforeKill"] = dominant_emotion_before
    else:
        kill_event["DominantEmotionBeforeKill"] = None

    if emotions_after:
        dominant_emotion_after = get_dominant_emotion(emotions_after[0]["Expression"])
        kill_event["DominantEmotionAfterKill"] = dominant_emotion_after
    else:
        kill_event["DominantEmotionAfterKill"] = None

with open(r'C:\\Users\Samuel\Desktop\\Libreface\\Json\\results_samu_updated.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Analysis completed and saved to results_samu_updated.json")
