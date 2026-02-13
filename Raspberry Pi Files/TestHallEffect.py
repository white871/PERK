import time
import gpiozero
import threading

hallEffect = []
for pin in [22, 24, 26, 28, 21, 23, 27, 29]:
    hallEffect.append(gpiozero.DigitalInputDevice(f"BOARD{pin}", pull_up = True))

def hallEffectRefresh():
    global hallEffect
    i = 0
    for sensor in hallEffect:
        print(str(sensor.value), end=' ')
        i += 1
    print('', end='\r')
    threading.Timer(0.1, hallEffectRefresh).start()

print("\n=============================")
print("LEAP Hall Effect Testing Tool")
print("=============================\n")
hallEffectRefresh()