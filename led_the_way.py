import RPi.GPIO as GPIO
import time
import sys,termios, tty, os

        
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

def moveDown():
    global sindex
    setSwitchOff(gpioInUses[sindex])
    sindex = sindex +1
    if(sindex == len(gpioInUses)):
        sindex = 0
    setSwitchOn(gpioInUses[sindex])
        
def moveUp():
    global sindex
    setSwitchOff(gpioInUses[sindex])
    sindex = sindex - 1
    if(sindex == -1):
        sindex = len(gpioInUses)-1
    setSwitchOn(gpioInUses[sindex])
def cycleQuick(gpioInUses):
    for gpio in gpioInUses:
        moveDown()
        time.sleep(0.2)
    #closeSwitches(gpioInUses)
    
def cycleQuickUp(gpioInUses):
    for gpio in gpioInUses:
        moveUp()
        time.sleep(0.2)
    #closeSwitches(gpioInUses)

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
    
GPIO.setmode(GPIO.BCM)
gpioInUses =[27,4,22]
sindex = 0
isPressed = 0
closeSwitches(gpioInUses)



GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
#GPIO.add_event_detect(20,GPIO.FALLING,callback=button_callback)
#GPIO.add_event_detect(20,GPIO.RISING,callback=button_callback_stop)
setSwitchOn(gpioInUses[sindex])             
while True:
    cycleQuick(gpioInUses)
  #  time.sleep(.75)
 #   moveDown()
  #  cycleQuickUp(gpioInUses)
  #  time.sleep(.75)
text = input()
closeSwitches(gpioInUses)
GPIO.cleanup()
