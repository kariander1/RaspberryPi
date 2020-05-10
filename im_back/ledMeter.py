import deviceManager
from deviceManager import PWMLED
import time
class ledMeter:
    __leds_pins=None# = [23,18,4,27,22]
    __PWMleds=[]
    __thresholds=[]
    __min_value=None
    __max_value=None
    current_value = None
    def __init__(self, led_pins=[]):
        self.__leds_pins = led_pins
        for pin in led_pins:
            self.__PWMleds.append(deviceManager.init_PWMled(pin))
    def add_led_pin(self,pin):
        self.__leds_pins.append(pin)
        self.__PWMleds.append(deviceManager.init_PWMled(pin))
    def add_PWMled(self,PWMled):
        self.__leds_pins.append(PWMled.pin)
        self.__PWMleds.append(PWMled)
    def set_value(self,value):
        minmax_changed = False
        if(self.__min_value is None or value<self.__min_value):
            self.__min_value = value
            minmax_changed=True
        if(self.__max_value is None or value>self.__max_value):
            self.__max_value = value
            minmax_changed=True
        
        if(minmax_changed == True):
            self.__calibrate()
            
        self.current_value = value
        self.__light_PWM()
    def __light_PWM(self):
        if(self.__min_value!= self.__max_value):
            thresholds_count = len(self.__thresholds)
            skip_led=False
                                   
            for i in range(thresholds_count):
                if(i<(thresholds_count-1) and self.__thresholds[i+1]>=self.current_value and self.__thresholds[i]<=self.current_value):
                    distance = self.__thresholds[i+1] - self.__thresholds[i]
                    prev_led_value = 1-(self.current_value-self.__thresholds[i])/distance
                    next_led_value = 1-(self.__thresholds[i+1]-self.current_value)/distance
                    
                    self.__PWMleds[i].value = prev_led_value
                    self.__PWMleds[i+1].value = next_led_value
                    skip_led=True                
                elif not skip_led:
                    self.__PWMleds[i].value =0
                else:
                    skip_led=False
    def __calibrate(self):
        self.__thresholds.clear()
        distance = (self.__max_value-self.__min_value)/(len(self.__PWMleds) -1)
        for i in range(len(self.__PWMleds)):
            self.__thresholds.append(self.__min_value+i*distance)
        
"""
deviceManager.print_gpio_board()

l = ledMeter()
l.add_led_pin(22)
l.add_led_pin(27)

l.add_led_pin(4)
l.add_led_pin(18)
l.add_led_pin(23)

l.set_value(0)
l.set_value(100)
l.set_value(50)
text=input()
for i in range(0,101):
    l.set_value(i)
    time.sleep(0.1)
    
"""