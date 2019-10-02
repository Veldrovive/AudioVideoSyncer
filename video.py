import numpy as np
import cv2
import os
import time
from random import randrange
import pickle

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
ret, frame = cap.read()
print(frame.shape[:2][::-1])

folder = "./temp"
video_output = os.path.join(folder, "video.mp4")
video_meta = os.path.join(folder, "video_meta.p")
video_final = os.path.join(folder, "video_final.p")

try:
	os.remove(video_output)
	os.remove(video_final)
except OSError:
	pass
out = cv2.VideoWriter(video_output,fourcc, 30, frame.shape[:2][::-1])

num_frames = 0
start_time = time.time()
end_time = start_time + 5
true_start = 0
true_end = 0
got_frame = False
while(time.time() < end_time and cap.isOpened()):
    ret, frame = cap.read()
    if frame is not None and not got_frame:
    	true_start = time.time()
    	got_frame = True
    	print("Started Getting Frames")
    if ret==True:
        cv2.imshow('frame',frame)

        out.write(frame)
        num_frames += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
true_end = time.time()
print("Stopped Getting frames after:",true_end-true_start,"seconds")
print("FPS:",num_frames/(end_time-start_time))

pickle.dump([true_start, true_end], open(video_meta, "wb"))

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
out = cv2.VideoWriter(video_final,fourcc, num_frames/(end_time-start_time), frame.shape[:2][::-1])

cap = cv2.VideoCapture(video_output)
while True:
	ret, frame = cap.read()
	if frame is None:
		break
	out.write(frame)
out.release()
cap.release()