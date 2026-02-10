# For Raspberry Pi
import time
import gpiozero
import subprocess
import threading
import wave
from piper import PiperVoice

from transliterateBinary import transliterateBin


def HallEffectRead():
    global currentLine
    global binArray
    global spaceBarPressed
    global newLinePressed
    while(True):
        if newLine.value:
            newLinePressed = 1
        elif newLinePressed:
            newLinePressed = 0
            currentLine += 1
        if spaceBar.value:
            spaceBarPressed = 1
            i = 0
            for sensor in hallEffect:
                if (sensor.value):
                    currentBinary = currentBinary[:i] + '1' + currentBinary[i + 1:]
                i += 1
            
        elif spaceBarPressed:
            spaceBarPressed = 0
            binArray[currentLine] += currentBinary
            
            if currentBinary == "000000":
                transliterate()
            currentBinary = '000000'
            f_bin = open("tempBin.txt", "w")
            for line in binArray:
                f_bin.write(line + "\n")
            f_bin.close()
        time.sleep(0.1)    
            
    
    
def transliterate():
    f_bin = open("tempBin.txt", "r")
    for line in f_bin.readlines():
        lastWord = transliterateBin(line)
        f_out = open("transliterateOutput.txt", "w")
        f_out.write("\n")
        f_out.close()
    f_bin.close()
    TTS(lastWord)

def TTS(word):
    with wave.open("output.wav", "wb") as f:
        voice.synthesize_wav(word, f)
        subprocess.run('aplay output.wav', shell = True)

model = "en_US-amy-low.onnx"
currentLine = 0
voice = PiperVoice.load(model)
open("output.txt", 'w').close()
with wave.open("output.wav", "wb") as f:
    voice.synthesize_wav("Ready", f)
    subprocess.run('aplay output.wav', shell = True)
spaceBarPressed = 0
newLinePressed = 0
HallEffect = [gpiozero.DigitalInputDevice(f"BOARD{pin}", pull_up = True) for pin in []]
HallEffectRead()
