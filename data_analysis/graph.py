import json
import matplotlib.pyplot as plt
import numpy as np

file_path = r"C:\Users\Samuel\Desktop\Libreface\Json\results_samu.json"
with open(file_path, 'r') as file:
    data = json.load(file)

emotions = ["Neutral", "Happiness", "Sadness", "Surprise", "Fear", "Disgust", "Anger", "Contempt"]
emotions_sum_victim = {emotion: {} for emotion in emotions}
emotions_sum_non_victim = {emotion: {} for emotion in emotions}
counts_victim = {}
counts_non_victim = {}

def add_emotions(emotion_dict, timestamp, is_victim):
    for emotion in emotions:
        if is_victim:
            if timestamp not in emotions_sum_victim[emotion]:
                emotions_sum_victim[emotion][timestamp] = 0
                counts_victim[timestamp] = 0
            emotions_sum_victim[emotion][timestamp] += emotion_dict[emotion]
            counts_victim[timestamp] += 1
        else:
            if timestamp not in emotions_sum_non_victim[emotion]:
                emotions_sum_non_victim[emotion][timestamp] = 0
                counts_non_victim[timestamp] = 0
            emotions_sum_non_victim[emotion][timestamp] += emotion_dict[emotion]
            counts_non_victim[timestamp] += 1

for kill in data["KillsInvolvingPlayer"]:
    victim = kill["Victim"]
    is_victim = (victim == "Thewizard45")
    kill_time = len(kill["EmotionsDuringKill"]) // 2  # A kill sempre ocorre na metade dos eventos (10 pra la 10 pra cá)
    for i, emotion_event in enumerate(kill["EmotionsDuringKill"]):
        timestamp = i - kill_time  
        add_emotions(emotion_event["Expression"], timestamp, is_victim)

# Calculate averages
average_emotions_victim = {emotion: [] for emotion in emotions}
average_emotions_non_victim = {emotion: [] for emotion in emotions}
time_range = sorted(set(counts_victim.keys()).union(set(counts_non_victim.keys())))

for emotion in emotions:
    for t in time_range:
        if t in counts_victim and counts_victim[t] > 0:
            average_emotions_victim[emotion].append(emotions_sum_victim[emotion][t] / counts_victim[t])
        else:
            average_emotions_victim[emotion].append(0)
        if t in counts_non_victim and counts_non_victim[t] > 0:
            average_emotions_non_victim[emotion].append(emotions_sum_non_victim[emotion][t] / counts_non_victim[t])
        else:
            average_emotions_non_victim[emotion].append(0)

time_range = np.array(time_range)  # Necessário para o plot
for emotion in emotions:
    plt.figure(figsize=(10, 5))
    plt.plot(time_range, average_emotions_victim[emotion], label='Victim (samu)')
    plt.plot(time_range, average_emotions_non_victim[emotion], label='Non-Victim')
    plt.title(f'Average {emotion} Before and After the Fight')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Average Intensity')
    plt.axvline(x=0, color='r', linestyle='--', label='Time of Kill')
    plt.legend()
    plt.grid(True)
    plt.show()
