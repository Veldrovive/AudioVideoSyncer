import os
import time
import numpy as np
import pickle
import sounddevice as sd
import soundfile as sf
import queue

folder = "./temp"
audio_output = os.path.join(folder, "audio.wav")
audio_meta = os.path.join(folder, "audio_meta.p")

global delta_time
global num_frames
data = list()
delta_time = None
num_frames = 0

dev_num = 0
devices = sd.query_devices()
print(devices)
print("Using:")
device_info = sd.query_devices(dev_num, 'input')
for prop in device_info:
	print(prop, device_info[prop])

time_map = {}
q = queue.Queue()

def callback(indata, frames, c_time, status):
	global delta_time
	global num_frames
	if delta_time is None:
		delta_time = time.time()-c_time.inputBufferAdcTime
	real_time = c_time.inputBufferAdcTime + delta_time
	time_map[real_time] = (num_frames+1, num_frames+len(indata))
	num_frames += len(indata)
	q.put(indata)

try:
	os.remove(audio_output)
except OSError:
	pass
with sf.SoundFile(audio_output, mode='x', samplerate=int(device_info['default_samplerate']), channels=device_info["max_input_channels"], subtype="PCM_24") as file:
	with sd.InputStream(samplerate=int(device_info['default_samplerate']), device=dev_num, channels=device_info["max_input_channels"], callback=callback) as stream:
		test_time = 10
		end_time = test_time + time.time()
		while time.time() < end_time or True:
			file.write(q.get())
			pickle.dump(time_map, open(audio_meta, "wb"))

full_size = os.path.getsize(audio_output) + os.path.getsize(audio_meta)
print("File has a size of:",full_size/1000000,"mb for a rate of",(full_size/1000000)/test_time,"mb/s or",test_time/(full_size/1000000000),"seconds per GB")