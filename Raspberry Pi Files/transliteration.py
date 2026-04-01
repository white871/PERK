# For Raspberry Pi
import time
import gpiozero
from gpiozero import DigitalInputDevice, DigitalOutputDevice, Button
import subprocess
import threading
import wave
from piper import PiperVoice

from transliterateBinary import transliterateBin

def powerDown():
  
def networkSearch():
      
def HallEffectRead():
     
            
    
    
def transliterate():
    

def TTS(word):
    

model = "en_US-amy-medium.onnx"
currentLine = 0
lastWordList = []
voice = PiperVoice.load(model)
open("output.txt", 'w').close()
with wave.open("output.wav", "wb") as f:
    voice.synthesize_wav("Ready", f)
    subprocess.run('aplay output.wav', shell = True)
binarry


#hallEffect = [DigitalInputDevice(f"BOARD{pin}", pull_up = True) for pin in [24, 26, 28, 23, 27, 29]]

hallEffect = [DigitalOutputDevice(f"BOARD{pin}", pull_up = True) for pin in [31,]]
mux_out = DigitalInputDevice(f"BOARD36", pull_up = True)
on_off = Button()
HallEffectRead()
