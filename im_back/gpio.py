import RPi.GPIO as GPIO
import sys

          
def close_switches(switches):
    for switch in switches:
        set_switch_off(switch)
def open_switches(switches):
    for switch in switches:
        set_switch_on(switch)
def set_switch_off(switchNum):
	GPIO.setup(switchNum,GPIO.OUT)
	GPIO.output(switchNum,GPIO.LOW)
def set_switch_on(switchNum):
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


def initialize_board(input_pins,output_pins):
    GPIO.seode(GPIO.BCM)
    for switch in input_pins:
        GPIO.setup(switch, GPIO.IN)
    for switch in output_pins:
        GPIO.setup(switch, GPIO.OUT)


