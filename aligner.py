import soundfile as sf
import numpy as np
import pickle
import os
import subprocess

folder = "./temp"
audio_input = os.path.join(folder, "audio.wav")
audio_meta = os.path.join(folder, "audio_meta.p")
audio_output = os.path.join(folder, "audio_final.wav")
video_input = os.path.join(folder, "video_final.mp4")
video_meta = os.path.join(folder, "video_meta.p")
video_output = os.path.join(folder, "final.mkv")


start_time, end_time = pickle.load(open("video_meta.p", "rb"))
print("Video Meta:",start_time, end_time)

time_data = pickle.load(open("audio_meta.p", "rb"))
times = np.array(list(time_data.keys()))
print("Audio Meta:",times[0],times[-1])
start_index = np.searchsorted(times, start_time, side="left")
end_index = np.searchsorted(times, end_time, side="left")
print(start_index, end_index)

start_frame, end_frame = time_data[times[start_index]][0], time_data[times[end_index]][0]
num_frames = end_frame-start_frame

sound = sf.SoundFile("audio.wav")
bit_rate = sound.samplerate
channels = sound.channels
subtype = sound.subtype

sound.seek(start_frame)
frames = sound.read(num_frames)

try:
	os.remove("audio_final.wav")
except OSError:
	pass
with sf.SoundFile("audio_final.wav", mode='x', samplerate=bit_rate, channels=channels, subtype=subtype) as file:
	print("Writing frames")
	file.write(frames)
	print("Wrote frames")

cmd = f'ffmpeg -y -i audio_final.wav  -r 30 -i {video_input}  -filter:a aresample=async=1 -c:a flac -c:v copy {video_output}'
subprocess.call(cmd, shell=True)                                     # "Muxing Done
print('Muxing Done')