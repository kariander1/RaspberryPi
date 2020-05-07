import RPi.GPIO as GPIO
import monitor
from monitor import Monitor
from gpiozero import Buzzer
from gpiozero import LED
from gpiozero import RGBLED
from gpiozero import PWMLED
from gpiozero import Button
from gpiozero import Servo
import gpio
import time
import sys
import threading
import math

LOGGING= False

pins_in_use=[]
devices=[]
devices_mapping ={
    
}
__gpio_mapping ={
    1 : "3.3V",
    2 : "5V",
    3 : "GPIO 2",
    4 : "5V",
    5 : "GPIO 3",
    6 : "GND",
    7 : "GPIO 4",
    8 : "GPIO 14",
    9 : "GND",
    10 : "GPIO 15",
    11 : "GPIO 17",
    12 : "GPIO 18",
    13 : "GPIO 27",
    14 : "GND",
    15 : "GPIO 22",
    16 : "GPIO 23",
    17 : "3.3V",
    18 : "GPIO 24",
    19 : "GPIO 10",
    20 : "GND",
    21 : "GPIO 9",
    22 : "GPIO 25",
    23 : "GPIO 11",
    24 : "GPIO 8",
    25 : "GND",
    26 : "GPIO 7",
    27 : "DNC",
    28 : "DNC",
    29 : "GPIO 5",
    30 : "GND",
    31 : "GPIO 6",
    32 : "GPIO 12",
    33 : "GPIO 13",
    34 : "GND",
    35 : "GPIO 19",
    36 : "GPIO 16",
    37 : "GPIO 26",
    38 : "GPIO 20",
    39 : "GND",
    40 : "GPIO 21",
}
def __init_board():
    GPIO.setmode(GPIO.BCM)

def log_message(text):
    if LOGGING is True:
        print(text)
def exit_program():    
    log_message("Exiting program..")    
    log_message("Threads alive : " +str(threading.active_count()))
    monitor.stop_monitors()
    log_message("Closing devices")
    for device in devices:
        destroyable = getattr(device, "destroy", None)
        if callable(destroyable):
            device.destroy()
       
    log_message("Closing used pins")
    for pin in pins_in_use:
        log_message("Closing pin N."+str(pin))
        gpio.set_switch_off(pin)
   
    #GPIO.cleanup() #Done by gpiozero
    log_message("Exit Done")
def init_sound_detector(listen_gpio,gnd_pin=-1,vcc_pin=-1,sound_detector_name="Sound Detector"):
    pins_in_use.append(listen_gpio)
    sound_detector = SoundDetector(listen_gpio,sound_detector_name)
    devices.append(sound_detector)
    devices_mapping[get_key("GPIO "+str(listen_gpio),__gpio_mapping)] =sound_detector_name
    devices_mapping[gnd_pin] = sound_detector_name+" GND"
    devices_mapping[vcc_pin] = sound_detector_name+" VCC"
    return sound_detector

def init_light_detector(listen_gpio,gnd_pin=-1,vcc_pin=-1,light_detector_name="Light Detector"):
    pins_in_use.append(listen_gpio)
    light_detector = LightDetector(listen_gpio,light_detector_name)
    devices.append(light_detector)
    devices_mapping[get_key("GPIO "+str(listen_gpio),__gpio_mapping)] =light_detector_name
    devices_mapping[gnd_pin] = light_detector_name+" GND"
    devices_mapping[vcc_pin] = light_detector_name+" VCC"
    return light_detector

def init_potentiometer(a_gpio,b_gpio,gnd_pin=-1,pot_name="Potentiometer"):
    pins_in_use.append(a_gpio)
    pins_in_use.append(b_gpio)
    pot = Potentimeter( a_gpio,b_gpio,pot_name)
    devices.append(pot)
    devices_mapping[get_key("GPIO "+str(a_gpio),__gpio_mapping)] =pot_name+" A"
    devices_mapping[get_key("GPIO "+str(b_gpio),__gpio_mapping)] =pot_name+" b"
    devices_mapping[gnd_pin] = pot_name+" GND"
    return pot

def init_motion_detector(listen_gpio,gnd_pin=-1,vcc_pin=-1,motion_detector_name="Motion Detector"):
    pins_in_use.append(listen_gpio)
    motion_detector = MotionDetector(listen_gpio,motion_detector_name)
    devices.append(motion_detector)
    devices_mapping[get_key("GPIO "+str(listen_gpio),__gpio_mapping)] =motion_detector_name
    devices_mapping[gnd_pin] = motion_detector_name+" GND"
    devices_mapping[vcc_pin] = motion_detector_name+" VCC"
    return motion_detector

def init_led(out_gpio,led_name="LED"):
    pins_in_use.append(out_gpio)
    led = LED(out_gpio)
    devices.append(led)
    devices_mapping[get_key("GPIO "+str(out_gpio),__gpio_mapping)] = led_name
    return led

def init_button(in_gpio,gnd_pin,button_name="Button"):
    pins_in_use.append(in_gpio)
    button = Button(in_gpio)
    devices.append(button)
    devices_mapping[get_key("GPIO "+str(in_gpio),__gpio_mapping)] = button_name
    devices_mapping[gnd_pin] =button_name+" GND"
    return button

def init_buzzer(out_gpio,gnd_pin,buzzer_name="Buzzer"):
    pins_in_use.append(out_gpio)
    buzzer = Buzzer(out_gpio)
    devices.append(buzzer)
    devices_mapping[get_key("GPIO "+str(out_gpio),__gpio_mapping)] = buzzer_name
    devices_mapping[gnd_pin] =buzzer_name+" GND"
    return buzzer
def init_servo(out_gpio,gnd_pin=-1,vcc_pin=-1,servo_name="Servo"):
    pins_in_use.append(out_gpio)
    servo = Servo(out_gpio)
    devices.append(servo)
    devices_mapping[get_key("GPIO "+str(out_gpio),__gpio_mapping)] =servo_name
    devices_mapping[gnd_pin] = servo_name+" GND"
    devices_mapping[vcc_pin] = servo_name+" VCC"
    return servo
def init_music_buzzer(out_gpio,gnd_pin,buzzer_name="Music Buzzer"):
    pins_in_use.append(out_gpio)
    buzzer = MusicBuzzer(out_gpio)
    devices.append(buzzer)
    devices_mapping[get_key("GPIO "+str(out_gpio),__gpio_mapping)] = buzzer_name
    devices_mapping[gnd_pin] =buzzer_name+" GND"
    return buzzer

def print_gpio_board():
    for pin_number in range(1,len(__gpio_mapping),2):
        left_device=""
        right_device=""
        if pin_number in devices_mapping:
            left_device = devices_mapping[pin_number]
        if (pin_number+1) in devices_mapping:
            right_device = devices_mapping[pin_number+1]        
        left_device=left_device.rjust(20, ' ')
        left_description = __gpio_mapping[pin_number].ljust(10, ' ')
        right_description = __gpio_mapping[pin_number+1].rjust(10, ' ')
        print(left_device ,' →o',str(pin_number).ljust(3)+" ",end = '')
        print(left_description,end = '')
        print(right_description,end = '')
        print(" "+str(pin_number+1).rjust(3),'o← ',right_device)
        

def get_key(val,dict): 
    for key, value in dict.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"


class LightMeasure:
     def __init__(self, duration, turned_on=True):
        self.duration = duration
        self.turned_on=turned_on
class LightDetector:
    __detectedLight=False
    __light_detect_interval = 100 #ms
    __listening=False
    __listen_monitor=None
    __start_calculating=False
    __key_frame=None
    key_frame_timeout=1000
    morse_measurements=[]
    def __init__(self, input_switch,light_detector_name="Light Detector"):
        log_message("Initializing "+ light_detector_name)
        self.name = light_detector_name
        self.__detectedLight=False
        self.__key_frame=None
        self.__listen_monitor = Monitor(self.name +" Light Monitor",self.light_change,self.__light_detect_interval)
        self.input_switch = input_switch
        self.output_switches = list()
        GPIO.setup(input_switch, GPIO.IN,GPIO.PUD_UP)           
        log_message("Initializing "+ light_detector_name+" Done")
        
    def set_detect_interval(self,interval):
        self.light_detect_interval = interval
        self.__listen_monitor.set_rate(interval)
    def start_listening(self):
        if not self.__listening:            
            self.__listen_monitor.start()
            self.__listening = True
            
    def add_trigger_pin(self,pin_number):
        self.output_switches.append(pin_number)
    def __add_light_measure(self,duration,was_on=True):
        self.morse_measurements.append(LightMeasure(duration,was_on))

    def light_change(self):
        input_result =GPIO.input(self.input_switch)
        if self.__start_calculating==True:   
          delta = time.time() -self.__key_frame
               
        if bool(input_result) is self.__detectedLight: # If there is a change on light detection
            if self.__start_calculating==True:                
                self.__add_light_measure(delta,self.__detectedLight)
            self.__key_frame = time.time()       
            self.__start_calculating=True
            
            if input_result==GPIO.LOW: # LOW for detecting light
                #log_message("Light Detected!")
                self.__detectedLight=True
                gpio.open_switches(self.output_switches)
            else:
                #log_message("Light Stopped!")
                self.__detectedLight=False
                gpio.close_switches(self.output_switches)
        elif self.__start_calculating is True: # Same light status
            if delta>self.key_frame_timeout/1000:
                self.__add_light_measure(delta,self.__detectedLight)
                self.__key_frame = time.time()       
    def destroy(self):
        self.__listen_monitor.join()
class MusicBuzzer:

    
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
    
    __output_pin=None
    __correct_tone=g[4]
    __incorrect_tone=c[2]
    tempo=0.5
    
    
    def __init__(self,output_pin):
        self.__output_pin = output_pin
        GPIO.setup(output_pin,GPIO.OUT)
    def play_note(self,note_frequency,duration):
        processThread = threading.Thread(target=self.__play_async, args=(note_frequency,duration));
        processThread.start()
    def __play_async(self,note_frequency,duration):
        tone = GPIO.PWM(self.__output_pin,100)
        tone.start(1)
        tone.ChangeFrequency(note_frequency)
        time.sleep(duration)
        tone.stop()
    def play_correct(self,duration=0.2):
        self.play_note(self.__correct_tone,duration)
    def play_incorrect(self,duration=0.2):
        self.play_note(self.__incorrect_tone,duration)
class SoundDetector:
    __listening=False
    sound_detect_interval = 100 #ms
    def __init__(self, input_switch,SoundDetector_name="Sound Detector"):
        log_message("Initializing "+ SoundDetector_name)
        self.name = SoundDetector_name
        self.detectedSound=False
        self.input_switch = input_switch
        self.output_switches = list()
        GPIO.setup(input_switch, GPIO.IN,GPIO.PUD_UP)
        #GPIO.add_event_detect(input_switch, GPIO.BOTH, bouncetime=self.sound_detect_interval)  # let us know when the pin goes HIGH or LOW
        #GPIO.add_event_callback(input_switch, self.sound_change)  # assign function to GPIO PIN, Run function on change
      
        log_message("Initializing "+ SoundDetector_name+" Done")
    def set_detect_interval(self,interval):
        self.sound_detect_interval = interval
    def add_trigger_pin(self,pin_number):
        self.output_switches.append(pin_number)
    def start_listening(self):
        Monitor(self.name +" Sound Monitor",self.sound_change,self.sound_detect_interval).start()
    def sound_change(self):
        input_result =GPIO.input(self.input_switch)
        #log_message(input_result)
        #log_message(self.detectedSound)
        #if bool(GPIO.input(self.input_switch)) is self.detectedSound:
        if input_result==GPIO.LOW: # LOW for detecting sound
            log_message("Sound Detected!")
            self.detectedSound=True
            gpio.open_switches(self.output_switches)
        else:
            log_message("Sound Stopped!")
            self.detectedSound=False
            gpio.close_switches(self.output_switches)
class MotionDetector:
    __listen_monitor=None
    __detected_motion=False
    __listening=False
    def __init__(self, input_switch,motion_detector_name="Sound Detector"):
        log_message("Initializing "+ motion_detector_name)
        self.name = motion_detector_name
        self.__listen_monitor = Monitor(self.name +" Light Monitor",self.motion_change,300)
        self.input_switch = input_switch
        self.output_switches = list()
        GPIO.setup(input_switch, GPIO.IN)           
        log_message("Initializing "+ motion_detector_name+" Done")

    def start_listening(self):
        if not self.__listening:            
            self.__listen_monitor.start()
            self.__listening = True
            
    def add_trigger_pin(self,pin_number):
        self.output_switches.append(pin_number)
    def motion_change(self):
        input_result =GPIO.input(self.input_switch)      
        
        if input_result==GPIO.HIGH: # HIGH for detecting light
            #log_message("Light Detected!")
            self.__detected_motion=True
            gpio.open_switches(self.output_switches)
        else:
            #log_message("Light Stopped!")
            self.__detected_motion=False
            gpio.close_switches(self.output_switches)
       
    def destroy(self):
        self.__listen_monitor.join()
class Potentimeter:
    a_pin =None
    b_pin =None
    output_pins = []
    current_pin_output=-1
    
    __sampling=False
    __changing_outputs=False
    
    __discharge_time=0.005
    __min_val=None
    __max_val=None
    __sample_frequency=None
    __val_range = 0
    __value_distance = 0
    __last_valid_measurement = None
    __change_request_count = 0
    __requests_for_changing = 3
    __calibrate_on_the_run=1
    __anomalies_count_for_acceptence = 4
    __anomailes_count = 0
    __anomaly_percent = 20
    def __init__(self, a_pin,b_pin,potentiometer_name="Potentiometer",frequency=20,min=20, max=30):        
        self.name =potentiometer_name
        
        self.a_pin=a_pin
        self.b_pin=b_pin
        self.__min_val = min
        self.__max_val = max
        if(self.__min_val is not None and self.__max_val is not None):
            self.__last_valid_measurement= (min+max)/2
        self.__sample_frequency = frequency
           
        gpio.set_switch_off(a_pin)
        gpio.set_switch_off(b_pin)
        self.__listen_monitor = Monitor(self.name +" Sample Monitor",self.__sample,(1/self.__sample_frequency)*1000)
    def start(self):
        self.start_changing_outputs()
        self.start_sampling()
    def stop(self):
        self.stop_sampling()
        self.stop_changing_outputs()
    def start_sampling(self):
        
        if(self.__listen_monitor.stopped()):
            self.__listen_monitor.resume()
        else:
            self.__listen_monitor.run()
        self.__sampling=True
    def stop_sampling(self):
        self.__listen_monitor.stop()  
        self.__sampling=False
    def start_changing_outputs(self):
        self.__changing_outputs=True
    def stop_changing_outputs(self):
        self.__changing_outputs=False
    def __cap_raw_value(self,raw_value):
        if(raw_value<self.__min_val):
            return self.__min_val
        elif(raw_value>self.__max_val):
            return self.__max_val
        return raw_value
            
    def __sample(self):
        raw_value =(self.__analog_read())  # Analog value of reading
        #output_text="Raw val: "+str(raw_value)
        anomaly_result = self.__not_anomaly(self.__last_valid_measurement,raw_value)
        if(anomaly_result == 1 or self.__anomailes_count== self.__anomalies_count_for_acceptence):
            ## Valid measurement
            
            self.__anomailes_count=0
            refined_value = self.__cap_raw_value(raw_value)
            if(refined_value!=raw_value and self.__calibrate_on_the_run):
                #There was redefinition and we allow calibrating on runtime
                self.calibrate(min(raw_value,self.__min_val),max(raw_value,self.__max_val))
                refined_value = raw_value #Treat anomaly as a valid measurement
            self.__last_valid_measurement = refined_value
            #if(raw_value<pot.min_val):
                #output_text+=(" Exceed low limit! "+str(raw_value))
             #   if(self.__calibrate_on_the_run):
              #      pot.calibrate(raw_value,pot.max_val)
               # else:
                #    raw_value = pot.min_val
           # elif(raw_value>pot.max_val):
                #output_text+=(" Exceed high limit! " +str(raw_value))
            #    if(self.__calibrate_on_the_run):
             #       pot.calibrate(pot.min_val,raw_value)
              #  else:
               #     raw_value = pot.max_val
           # output_text+=" Refined val: "+str(raw_value)
        
            self.apply_device_logic(refined_value)             
                
        else:
            self.__anomailes_count=self.__anomailes_count+1
            #output_text+= (" Anomaly "+str(refined_value)+ " is "+str(anomaly_result)+" from "+str(last_valid_measurement)+" Total anomalies "+ str(anomaly_count))
        #print(output_text)
    def apply_device_logic(self,currnet_measurement):
        device_index = math.floor(((currnet_measurement-self.__min_val)/self.__value_distance))
        #output_text+=(" Led to light: "+str(device_index))
        if(self.output_pins[device_index]!=self.current_pin_output):
            self.__change_request_count=self.__change_request_count+1
        else:
            self.__change_request_count=0
            
        if(self.__change_request_count == self.__requests_for_changing):
            self.__change_request_count=0
            if(self.__changing_outputs):
                if(self.current_pin_output != -1):
                    gpio.set_switch_off(self.current_pin_output)
            gpio.set_switch_on(self.output_pins[device_index])    
            self.current_pin_output=self.output_pins[device_index]    
            
    def calibrate(self,min_value=-1,max_value=-1):
        #    print("Calibrating")
        #  openSwitches(leds)
            if(min_value!=-1):
                self.__min_val=min_value
            if(max_value!=-1):
                self.__max_val=max_value
            self.__val_range = self.__max_val - self.__min_val+1 # the +1 is becuase the analog can be also the highest limit
            zones = len(self.output_pins)
            self.__value_distance= (self.__val_range)/zones
      #      print(str(zones)+" ranges")
     #       for x in range(zones):
     #           print("Threshold "+str(x)+" "+str(self.__min_val+self.__value_distance*(1+x)))
            #closeSwitches(leds)
        #    print("Calibration Done")
    def add_output_pin(self,out_pin):
        self.output_pins.append(out_pin)
        self.calibrate()
    
    def __discharge(self):
        GPIO.setup(self.a_pin, GPIO.IN)
        GPIO.setup(self.b_pin, GPIO.OUT)
        GPIO.output(self.b_pin, False)
        time.sleep(self.__discharge_time)

    def __charge_time(self):
        GPIO.setup(self.b_pin, GPIO.IN)
        GPIO.setup(self.a_pin, GPIO.OUT)
        count = 0
        GPIO.output(self.a_pin, True)
        while not GPIO.input(self.b_pin):
            count = count + 1
        return count

    def __analog_read(self):
        self.__discharge()
        return self.__charge_time()
    def __calc_deviation(self,orig_val,new_val):
        dif = abs(new_val-orig_val)
        deviation = (dif/self.__val_range)*100
        return deviation
    def __not_anomaly(self,orig_val,new_val):
        
        deviation = self.__calc_deviation(orig_val,new_val)
        if((deviation)>self.__anomaly_percent): # Is Anomaly
            return deviation
        else:
            return 1
        
        
__init_board()