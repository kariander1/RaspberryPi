import RPi.GPIO as GPIO
import time
import sys
import math
import csv
import datetime
from picamera import PiCamera

def closeSwitches(switches):
    for switch in switches:
        setSwitchOff(switch)
        
def setSwitchOff(switchNum):
	GPIO.setup(switchNum,GPIO.OUT)
	GPIO.output(switchNum,GPIO.LOW)
	
def setSwitchOn(switchNum):
	GPIO.setup(switchNum,GPIO.OUT)
	GPIO.output(switchNum,GPIO.HIGH)
def openSwitchesDuration(switches,duration):
    for switch in switches:
        setSwitchOn(switch)
    time.sleep(duration)
    for switch in switches:
        setSwitchOff(switch)
def openSwitches(switches):
    for switch in switches:
        setSwitchOn(switch)
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

def button_callback(channel):
    global sindex
    global isPressed
    if(isPressed == 0):
        isPressed = 1
        setSwitchOff(gpioInUses[sindex])
        sindex = sindex +1
        if(sindex == len(gpioInUses)):
            sindex = 0
        #openSwitches(gpioInUses)
        print("Opening PIN "+ str(gpioInUses[sindex]))
        setSwitchOn(gpioInUses[sindex])
        #time.sleep(0.5)
        isPressed = 0
    
    
class distance_meter:
    def __init__(self, trigger_pin, echo_pin):
        print("Initializing Distance Sensor")
        self.PIN_TRIGGER = trigger_pin
        self.PIN_ECHO = echo_pin
        closeSwitches([self.PIN_TRIGGER,self.PIN_ECHO])
        
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        time.sleep(2)
        print("Initializing Distance Sensor - Done")
        
GPIO.setmode(GPIO.BCM)


leds = [18,27,4,17]
closeSwitches(leds)
dist = distance_meter(16,12)
#TLLDs
one_time_capture = 1
measure_interval = 20000000
sleep_interval = 1/measure_interval

log_name = "dist_"+str(datetime.datetime.now())+".csv"

camera = PiCamera()
camera.start_preview()
with open(log_name, 'w') as writeFile:
    writer = csv.writer(writeFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Date Time' ,'Pulse Start', 'Pulse End','Pulse Duration','Distance','Delta From Last'])


    while(1==1):
        GPIO.output(dist.PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(dist.PIN_TRIGGER, GPIO.LOW)



        while GPIO.input(dist.PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(dist.PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        distance = round(pulse_duration * 17150, 2)
        print ("Distance:",distance,"cm")
        openSwitch = 0
##        if(distance > 7):
##            print ("Rasp is far")
##        elif (distance > 5):
##            print ("Rasp is close")
##        elif (distance > 3):
##            print ("Rasp is fucked")
        if(distance < 3):
            
            openSwitch=1
        if(openSwitch):
            openSwitches(leds)
            if(one_time_capture):
                one_time_capture=0
                print ("Captured")
                camera.capture('/home/pi/Desktop/image.jpg')
        else:
            closeSwitches(leds)
        
        writer.writerow([time.time(),pulse_start_time,pulse_end_time,pulse_duration,distance])
        time.sleep(0.1)

writeFile.close()
GPIO.cleanup()
