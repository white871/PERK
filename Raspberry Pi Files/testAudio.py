import subprocess
import wave
from piper import PiperVoice
import time
import gpiozero, board, busio, digitalio
import adafruit_tlv320
#from smbus3 import SMBus
model = "en_US-amy-low.onnx"
#time_obj = time.time()
addr = 0x18
reset = digitalio.DigitalInOut(board.D4)
reset.direction = digitalio.Direction.OUTPUT
reset.value = False

#bus = SMBus(1)
## Setup DAC

time.sleep(0.1)
reset.value = True
#time.sleep(1000)
'''
Failed attempt at trying to write registers , if you wanna try this and suffer, be my guest. 

bus.write_byte_data(addr, 0, 0)
# Set PLL Stuff

bus.write_byte_data(addr, 6, 8) 
bus.write_byte_data(addr, 7, 0)
bus.write_byte_data(addr, 8, 0)
bus.write_byte_data(addr, 4, 0x03)
bus.write_byte_data(addr, 5, 0x91) # Power up PLL
time.sleep(0.01)
# Setup DAC and Divider
bus.write_byte_data(addr, 11, 0x84)
bus.write_byte_data(addr, 12, 0x88)
bus.write_byte_data(addr, 13, 0x00)
bus.write_byte_data(addr, 14, 0x80)


# Power DAC
bus.write_byte_data(addr, 63, 0xD4) # Enable both channels, set both datapaths to between channels (since mono)

# Unmute DAC
bus.write_byte_data(addr, 64, 0x00) # Unmute both channels, set right channel as programmed volume
bus.write_byte_data(addr, 65, 0)
bus.write_byte_data(addr, 66, 0x00) # Set right volume 

bus.write_byte_data(addr, 27, 0x00)

bus.write_byte_data(addr, 0, 1) # go to page 1
bus.write_byte_data(addr, 32, 0x86) # turn on speaker
bus.write_byte_data(addr, 35, 0x44)
bus.write_byte_data(addr, 38, 0x80) #Setup speaker 
bus.write_byte_data(addr, 42, 0x1C)
 '''

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_tlv320.TLV320DAC3100(i2c)

dac.configure_clocks(sample_rate=44100, bit_depth = 16, mclk_freq = 0)
#dac.mclk_freq = 0
dac.speaker_output = True
dac.speaker_volume = 0
dac.dac_volume = 0
# Load Model
init_time = time.time()
voice = PiperVoice.load(model)
load_time = time.time()
print(f"Time to load : {load_time - init_time}")

init_time = time.time()
with wave.open("output.wav", "wb") as f:
	voice.synthesize_wav("We did it everybody!", f)
	print(f"Time to play (Many words): {time.time() - init_time}")
	subprocess.run('aplay -D plughw:0,0 output.wav', shell = True)
	
with wave.open("output.wav", "wb") as f:
	init_time = time.time()
	voice.synthesize_wav("Okay",f)
	subprocess.run('aplay -D plughw:0,0 output.wav', shell = True)
	print(f"Time to play (1 word): {time.time() - init_time}")

#while True:

	#text = input("Word to say \n")
	#in_time = time.time()
	#with wave.open("output.wav", "wb") as f:
		#voice.synthesize_wav(text, f)
		#subprocess.run('aplay output.wav', shell = True)
		#out_time = time.time()
		#print(f"Time to speak: {out_time - in_time}")
