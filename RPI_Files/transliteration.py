# For Raspberry Pi
import time
import gpiozero
from gpiozero import DigitalInputDevice, DigitalOutputDevice, Button
import subprocess
import threading
import wave
from piper import PiperVoice

from transliterateBinary import transliterateBin
def beep_beep(freq1, freq2):
    subprocess.run(f'( speaker-test -t sine -f {freq1} )& pid=$! ; sleep 0.2s ; kill -9 $pid', shell = True)
    subprocess.run(f'( speaker-test -t sine -f {freq2} )& pid=$! ; sleep 0.2s ; kill -9 $pid', shell = True)

def powerDown():
    beep_beep(1500, 1000)
    subprocess.run('sudo shutdown now', shell = True)
    
def networkSearch():
    beep_beep(1500, 1500)
    out = subprocess.check_output('sudo nmcli -t -f SSID,SIGNAL dev wifi list', shell = True)
    print(out.decode('utf-8'))
    for net in out.decode('utf-8').split("\n"):
        net = net.split(":")
        if net[0][0:5] == "perk-":
            subprocess.run(f'sudo nmcli dev wifi connect {net[0]} password perk12345', shell = True)
            beep_beep(1000, 1500)
            return
    beep_beep(1000,1000)

    
def HallEffectRead(hallEffect, out):
    outputnum = ""
    for i in range(8):
        for j in range(3):
            hallEffect[j].on() if (i >> j) & 1 else hallEffect[j].off()
        time.sleep(0.001)
        outputnum += str(out.value)
    return outputnum
    

def TTS(word, voice):
    try:
        with wave.open("output.wav", "wb") as f:
            voice.synthesize_wav(word, f)
            subprocess.run('aplay output.wav', shell = True)
    except: 
        pass    
        
model = "en_US-amy-medium.onnx"
currentLine = 0
lastWordList = []
voice = PiperVoice.load(model)
open("output.txt", 'w').close()
with wave.open("output.wav", "wb") as f:
    voice.synthesize_wav("Ready", f)
    subprocess.run('aplay output.wav', shell = True)

hallEffect = [DigitalOutputDevice(f"BOARD{pin}", active_high = True) for pin in [31, 33, 37]]
mux_out = DigitalInputDevice(f"BOARD36", pull_up = True)
on_off = Button(23)
pair = Button(24)

on_off.when_pressed = powerDown
pair.when_pressed = networkSearch

binArray = []
space_press = 0
line_press = 0
current_line = 0
lastWord = ""
while True:
    output = HallEffectRead(hallEffect, mux_out)
    newline = int(output[3])
    space = int(output[4])
    keys = output[0:3] + output[5:8]
	#keys = output[3] + output[2] + output[1] + output[5:8]
    if space:
        space_press = 1
        currentBinary = keys
    elif space_press:
        print(currentBinary)
        if lastWord and currentBinary == "000000": 
            TTS(lastWord, voice)
        space_press = 0
        if current_line >= len(binArray):
            binArray.append(currentBinary)
        else:
            binArray[current_line] += currentBinary
            print(binArray[current_line])
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
