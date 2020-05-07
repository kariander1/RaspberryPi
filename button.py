import RPi.GPIO as GPIO
import time
import sys
import threading
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
    print("button released")
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
    

def button_callback_stop(channel):
    print("button released")
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
        
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
def loop1_10(button_pin_number,switch_to_toggle):
    global exit
    is_pressed=False
    while(not exit):
        input_state = GPIO.input(button_pin_number) #false means button is pressed
        #if(input_state == False):
        #    setSwitchOn(17)
        #else :
        #    setSwitchOff(17)
        if(is_pressed == input_state):
            #print("Toggle")
            #toggleSwitch(switch_to_toggle)
            if(not is_pressed):
                setSwitchOn(switch_to_toggle)
            else:
                setSwitchOff(switch_to_toggle)
        is_pressed = not(input_state)

exit = False
GPIO.setmode(GPIO.BCM)
gpioInUses =[14,18,27,4,22,17]
sindex = 0
isPressed = 0
#closeSwitches(gpioInUses)
c =0 
  
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
processThread  =threading.Thread(target=loop1_10,args=[20,17]) #17 - buzzer
#GPIO.add_event_detect(20,GPIO.FALLING,callback=button_callback, bouncetime=300)  
#GPIO.add_event_detect(20,GPIO.FALLING,callback=button_callback_stop)
             
processThread.start()
text = input()

exit = True
processThread.join()
closeSwitches(gpioInUses)
GPIO.cleanup()
