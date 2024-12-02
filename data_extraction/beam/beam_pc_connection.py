import csv
import time
from eyeware.client import TrackerClient

tracker = TrackerClient()

with open('tracking_data_lol_25.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'HeadPose_X', 'HeadPose_Y', 'HeadPose_Z', 'ScreenGaze_X', 'ScreenGaze_Y','GazeLost'])

    while True:
        if tracker.connected:
            head_pose = tracker.get_head_pose_info()
            if not head_pose.is_lost:
                head_pose_translation = head_pose.transform.translation
                print(f"Head Pose: {head_pose_translation}")
            screen_gaze = tracker.get_screen_gaze_info()
            print(f"Screen Gaze: {screen_gaze.x}, {screen_gaze.y}")
                
            timestamp = time.time()
            head_pose_x = head_pose_translation[0]
            head_pose_y = head_pose_translation[1]
            head_pose_z = head_pose_translation[2]
            screen_gaze_x = screen_gaze.x
            screen_gaze_y = screen_gaze.y
            gaze_lost = screen_gaze.is_lost

            writer.writerow([timestamp, head_pose_x, head_pose_y, head_pose_z, screen_gaze_x, screen_gaze_y,gaze_lost])
            print(f"Saved data at {timestamp}")
                
            time.sleep(1)
        else:
            print("No connection with tracker server")
            time.sleep(2)
