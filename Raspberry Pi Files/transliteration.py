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
    subprocess.run('( speaker-test -t sine -f 1500 )& pid=$! ; sleep 0.2s ; kill -9 $pid')
    subprocess.run('( speaker-test -t sine -f 1000 )& pid=$! ; sleep 0.2s ; kill -9 $pid')
    subprocess.run('sudo shutdown now')
    
def networkSearch():
    
def HallEffectRead(hallEffect, out):
    outputnum = ""
    for i in range(8):
        for j in range(3):
            hallEffect[j].on() if (i >> j) & 1 else hallEffect[j].off()
        time.sleep(0.001)
        outputnum += str(out.value)
    return outputnum
    

def TTS(word, voice):
    with wave.open("output.wav", "wb") as f:
        voice.synthesize_wav(word, f)
        subprocess.run('aplay output.wav', shell = True)
        
        
model = "en_US-amy-medium.onnx"
currentLine = 0
lastWordList = []
voice = PiperVoice.load(model)
open("output.txt", 'w').close()
with wave.open("output.wav", "wb") as f:
    voice.synthesize_wav("Ready", f)
    subprocess.run('aplay output.wav', shell = True)

hallEffect = [DigitalOutputDevice(f"BOARD{pin}", pull_up = True) for pin in [31, 33, 37]]
mux_out = DigitalInputDevice(f"BOARD36", pull_up = True)
on_off = Button(23)
pair = Button(24)
binArray = []
space_press = 0
line_press = 0
current_line = 0
lastWord = ""
while True:
    output = HallEffectRead(hallEffect, mux_out)
    newline = int(output[0])
    space = int(output[4])
    keys = output[1:3] + output[5:7]
    if space:
        space_press = 1
    elif space_press:
        if lastWord and keys == "000000": 
            TTS(lastWord, voice)
        space_press = 0
        binArray[current_line] += keys
        with open("tempbin.txt", 'w') as f:
            for line in binArray:
                f.write(line + '\n')
                lastWord = transliterateBin(line)
                with open("transliterateOutput.txt", 'a') as f_out:
                    f_out.write("\n")               
    if newline:
        line_press = 1
    elif line_press:
        line_press = 0
        current_line += 1
   
    time.sleep(0.1)