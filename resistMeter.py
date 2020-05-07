import RPi.GPIO as GPIO
import time
import sys
import math

        
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
    
GPIO.setmode(GPIO.BCM)
gpioInUses =[16,12]
leds = [3,2,4,27,22]
closeSwitches(gpioInUses)
closeSwitches(leds)
a_pin = 16
b_pin = 12

def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)

def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
        count = count + 1
    return count

def analog_read():
    discharge()
    return charge_time()

def not_anomaly(orig_val,new_val,vals_range):
    dif = abs(new_val-orig_val)
    dev = (dif/vals_range)*100
    if((dev)>anomaly_percent): # Is Anomaly
        return dev
    else:
        return 1
class Potentimeter:
  def __init__(self, min, max):
      self.calibrate(min,max)
          
  def calibrate(self, min,max):
        print("Calibrating")
      #  openSwitches(leds)
        self.min_val = min
        self.max_val = max
        self.val_range = self.max_val - self.min_val+1# the +1 is becuase the analog can be also the highest limit
        self.zones = len(leds)
        self.d= (self.val_range)/self.zones
        print(str(self.zones)+" ranges")
        for x in range(self.zones):
            print("Threshold "+str(x)+" "+str(self.min_val+self.d+self.d*x))
        #closeSwitches(leds)
        print("Calibration Done")
#DO: calibarate
#Number of anomalies to actualy change
#plasy with time sleep

pot = Potentimeter(0,1)
#calibrate(5,100)
currentIndex=0
last_valid_measurement = (pot.min_val +pot.max_val)/2
anomaly_count =0

#TLLD :
samplingFrequency = 100
calibrateInProcess = 1
numberOfAnomalies=3
anomaly_percent = 20



interval = 1/samplingFrequency
while True:
    a2d =(analog_read())
    output_text="Raw val: "+str(a2d)
    anomaly_result = not_anomaly(last_valid_measurement,a2d,pot.val_range)
    if(anomaly_result == 1 or anomaly_count== numberOfAnomalies):
        last_valid_measurement = a2d
        anomaly_count=0
        if(a2d<pot.min_val):
            output_text+=(" Exceed low limit! "+str(a2d))
            if(calibrateInProcess):
                pot.calibrate(a2d,pot.max_val)
            else:
                a2d = pot.min_val
        elif(a2d>pot.max_val):
            output_text+=(" Exceed high limit! " +str(a2d))
            if(calibrateInProcess):
                pot.calibrate(pot.min_val,a2d)
            else:
                a2d = pot.max_val
        output_text+=" Refined val: "+str(a2d)
    
        ledIndex = math.floor(((a2d-pot.min_val)/pot.d))
        output_text+=(" Led to light: "+str(ledIndex))
        if(ledIndex!=currentIndex):
            setSwitchOff(leds[currentIndex])
            setSwitchOn(leds[ledIndex])
            currentIndex = ledIndex
    else:
        anomaly_count=anomaly_count+1
        output_text+= (" Anomaly "+str(a2d)+ " is "+str(anomaly_result)+" from "+str(last_valid_measurement)+" Total anomalies "+ str(anomaly_count))
    print(output_text)
    time.sleep(interval)
    
GPIO.cleanup()
