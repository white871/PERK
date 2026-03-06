import subprocess
import wave
from piper import PiperVoice
import time
model = "en_US-amy-low.onnx"
#time_obj = time.time()

init_time = time.time()
voice = PiperVoice.load(model)
load_time = time.time()

print(f"Time to load : {load_time - init_time}")

with wave.open("output.wav", "wb") as f:
	voice.synthesize_wav("We did it everybody", f)
	subprocess.run('aplay output.wav', shell = True)
	
#while True:
	#text = input("Word to say \n")
	#in_time = time.time()
	#with wave.open("output.wav", "wb") as f:
		#voice.synthesize_wav(text, f)
		#subprocess.run('aplay output.wav', shell = True)
		#out_time = time.time()
		#print(f"Time to speak: {out_time - in_time}")
