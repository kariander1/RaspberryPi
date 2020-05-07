import RPi.GPIO as GPIO
import time
import sys
from gpiozero import Buzzer

          
def closeSwitches(switches):
    for switch in switches:
        setSwitchOff(switch)
        
def setSwitchOff(switchNum):
	GPIO.setup(switchNum,GPIO.OUT)
	GPIO.output(switchNum,GPIO.LOW)
	
def setSwitchOn(switchNum):
	GPIO.setup(switchNum,GPIO.OUT)
	GPIO.output(switchNum,GPIO.HIGH)
	
def openSwitch(switchNum, duration):
#	print("About On")
	toggleSwitch(switchNum)
#	print(duration)
#	print("Sleep")
	time.sleep(duration)
#	print("AboutOff")
	toggleSwitch(switchNum)
def toggleSwitch(switchNum):
	GPIO.setup(switchNum,GPIO.IN)
	state = GPIO.input(switchNum)
	GPIO.setup(switchNum,GPIO.OUT)
#	print (state)
	if (state):
		GPIO.output(switchNum,GPIO.LOW)
	else:
		GPIO.output(switchNum,GPIO.HIGH)
		
def playScale(scale, pause):
    for i in range(0, 5):
        for note in scale:
            tone1.ChangeFrequency(note[i])
            time.sleep(pause)
    tone1.stop()

def playSong(songnotes, songbeats, tempo):
    tone1.ChangeDutyCycle(30)
    for i in range(0, len(songnotes)):
        tone1.ChangeFrequency(songnotes[i])
        time.sleep(songbeats[i]*tempo)
    tone1.ChangeDutyCycle(0)
    
    
c = [32, 65, 131, 262, 523]
db= [34, 69, 139, 277, 554]
d = [36, 73, 147, 294, 587]
eb= [37, 78, 156, 311, 622]
e = [41, 82, 165, 330, 659]
f = [43, 87, 175, 349, 698]
gb= [46, 92, 185, 370, 740]
g = [49, 98, 196, 392, 784]
ab= [52, 104, 208, 415, 831]
a = [55, 110, 220, 440, 880]
bb= [58, 117, 223, 466, 932]
b = [61, 123, 246, 492, 984]

cmajor = [c, d, e, f, g, a, b]
aminor = [a, b, c, d, e, f, g]


GPIO.setmode(GPIO.BCM)
gpioInUses =[17]
starwars_notes = [c[1], g[1], f[1], e[1], d[1], c[2], g[1], f[1], e[1], d[1], c[2], g[1],f[1], e[1], f[1], d[1]]
starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]
GPIO.setup(17,GPIO.OUT)
tone1 = GPIO.PWM(17,100)
tone1.start(1)
playSong(starwars_notes, starwars_beats, 0.5)
GPIO.cleanup()
