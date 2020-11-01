import RPi.GPIO as GPIO
import monitor
from monitor import Monitor
from gpiozero import Buzzer
from gpiozero import LED
from gpiozero import RGBLED
from gpiozero import PWMLED
from gpiozero import Button
from gpiozero import Servo
from gpiozero import DistanceSensor
from gpiozero import OutputDevice as Stepper
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

def init_distance_sensor(echo_gpio,trigger_gpio,gnd_pin=-1,vcc_pin=-1,sensor_name="Distance Sensor"):
    pins_in_use.append(echo_gpio)
    pins_in_use.append(trigger_gpio)
    distance_sensor = DistanceMeter(echo_gpio,trigger_gpio)
    devices.append(distance_sensor)
    devices_mapping[get_key("GPIO "+str(echo_gpio),__gpio_mapping)] =sensor_name+" ECHO"
    devices_mapping[get_key("GPIO "+str(trigger_gpio),__gpio_mapping)] =sensor_name+" TRIG"
    devices_mapping[gnd_pin] = sensor_name+" GND"
    devices_mapping[vcc_pin] = sensor_name+" VCC"
    return distance_sensor

def init_led(out_gpio,led_name="LED"):
    pins_in_use.append(out_gpio)
    led = LED(out_gpio)
    devices.append(led)
    devices_mapping[get_key("GPIO "+str(out_gpio),__gpio_mapping)] = led_name
    return led

def init_PWMled(out_gpio,gnd_pin=-1,led_name="PWM LED"):
    pins_in_use.append(out_gpio)
    led = PWMLED(out_gpio)
    devices.append(led)
    devices_mapping[get_key("GPIO "+str(out_gpio),__gpio_mapping)] = led_name
    devices_mapping[gnd_pin] = led_name+" GND"
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
def init_servo_gpiozero(out_gpio,gnd_pin=-1,vcc_pin=-1,servo_name="Servo gpio zero"):
    pins_in_use.append(out_gpio)
    servo = Servo(out_gpio)
    devices.append(servo)
    devices_mapping[get_key("GPIO "+str(out_gpio),__gpio_mapping)] =servo_name
    devices_mapping[gnd_pin] = servo_name+" GND"
    devices_mapping[vcc_pin] = servo_name+" VCC"
    return servo
def init_stepper_motor(out1,out2,out3,out4,vcc_pin=-1,gnd_pin=-1,stepper_name ="Stepper"):
    pins_in_use.append(out1)
    pins_in_use.append(out2)
    pins_in_use.append(out3)
    pins_in_use.append(out4)
    motor = StepMotor(out1,out2,out3,out4)
    devices.append(motor)
    devices_mapping[get_key("GPIO "+str(out1),__gpio_mapping)] =stepper_name
    devices_mapping[get_key("GPIO "+str(out2),__gpio_mapping)] =stepper_name
    devices_mapping[get_key("GPIO "+str(out3),__gpio_mapping)] =stepper_name
    devices_mapping[get_key("GPIO "+str(out4),__gpio_mapping)] =stepper_name
    devices_mapping[gnd_pin] = stepper_name+" GND"
    devices_mapping[vcc_pin] = stepper_name+" VCC"
    return motor
def init_servo(out_gpio,gnd_pin=-1,vcc_pin=-1,servo_name="Servo"):
    pins_in_use.append(out_gpio)
    servo = MicroServer(out_gpio)
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
class DistanceMeter:
    __sonic_speed = 34300 #cm/s
    __echo_timeout =1 #sec
    __max_measure_retry=3
    __trigger_pin=None
    __echo_pin=None
    def __init__(self,echo_pin , trigger_pin):
        print("Initializing Distance Sensor")
        self.__trigger_pin = trigger_pin
        self.__echo_pin = echo_pin
         
        GPIO.setup(self.__trigger_pin, GPIO.OUT)
        GPIO.setup(self.__echo_pin, GPIO.IN)
        GPIO.output(self.__trigger_pin, GPIO.LOW)
        time.sleep(2)
        print("Initializing Distance Sensor - Done")
        
    def take_measurements(self,duration,measure_timeout=None):
        if(measure_timeout == None):
            measure_TO = duration
        else:
            measure_TO = measure_timeout
        distance = 0
        
        num_of_measurements =0
        measure_duration = 0
        measure_start = time.time()
        while measure_duration<=duration :
            current_measurement = self.take_measurement(measure_TO)
            if(current_measurement is None):
                return None
            distance = (distance *num_of_measurements +current_measurement )/(num_of_measurements+1)
            num_of_measurements+=1
            measure_duration = time.time() - measure_start
        if(distance==0):
            return None
        return distance

    def take_measurement(self,timeout=None):
        if(timeout is None):
            timeout = self.__echo_timeout/self.__max_measure_retry
        else:
            timeout/=self.__max_measure_retry
        
        repeat =True
        retries=0
        
        while(repeat is True and retries < self.__max_measure_retry ):
            repeat=False
            GPIO.output(self.__trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.__trigger_pin, GPIO.LOW)

            pulse_start_time = 0
            pulse_end_time = 0

        
            wait_pulse = time.time()
            while GPIO.input(self.__echo_pin)==0 and not repeat:
                pulse_start_time = time.time()
                if((time.time() - wait_pulse) >=timeout):
                    #print("TO echo 0")
                    repeat=True
            while GPIO.input(self.__echo_pin)==1 and not repeat:
                pulse_end_time = time.time()
                if((time.time() - wait_pulse) >=timeout):
                    #print("TO echo 1")
                    repeat=True
            if(pulse_start_time ==0 or pulse_end_time == 0): #Invalid measurement
                repeat=True
            
            if(repeat == True):
                retries+=1
        
        if(retries == self.__max_measure_retry):
            return None
        pulse_duration = pulse_end_time - pulse_start_time

        distance = round((pulse_duration * self.__sonic_speed)/2, 2)
     #   print(distance)
        return distance
class StepMotor:
    __step_pins=[]
    __step_speed = 2 #1 or 2
    __steps_for_revolution = 4096/__step_speed
    
    __steps_angle_ratio = __steps_for_revolution/360
    __seq = [[1,0,0,1], # Define step sequence as shown in manufacturers datasheet
             [1,0,0,0], 
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1]]
    __wait_time = 0.004
    def __init__(self,out1,out2,out3,out4):
        IN1 = Stepper(out1)
        IN2 = Stepper(out2)
        IN3 = Stepper(out3)
        IN4 = Stepper(out4)
        self.__step_pins = [IN1,IN2,IN3,IN4] # Motor GPIO pins</p><p>
    def rotate_steps(self,steps,antiCW=True):
        stepDir = self.__step_speed
        if(not antiCW):
            stepDir *= -1
        stepCount = len(self.__seq)
        step_counts=0
        stepCounter = 0
        steps_to_move=steps
        while step_counts<steps_to_move:            # Start main loop
            for pin in range(0,len(self.__step_pins)):
                xPin=self.__step_pins[pin]          # Get GPIO
                if self.__seq[stepCounter][pin]!=0:
                    xPin.on()
                else:
                    xPin.off()
            stepCounter += stepDir
            if (stepCounter >= stepCount):
                stepCounter = 0
            if (stepCounter < 0):
                stepCounter = stepCount+stepDir
            step_counts+=1
            print(step_counts)
            time.sleep(self.__wait_time)     # Wait before moving on
    def rotate(self,degrees,antiCW=True):
        stepDir = self.__step_speed
        if(not antiCW):
            stepDir *= -1
        stepCount = len(self.__seq)
        step_counts=0
        stepCounter = 0
        steps_to_move=degrees*self.__steps_angle_ratio
        while step_counts<steps_to_move:            # Start main loop
            for pin in range(0,len(self.__step_pins)):
                xPin=self.__step_pins[pin]          # Get GPIO
                if self.__seq[stepCounter][pin]!=0:
                    xPin.on()
                else:
                    xPin.off()
            stepCounter += stepDir
            if (stepCounter >= stepCount):
                stepCounter = 0
            if (stepCounter < 0):
                stepCounter = stepCount+stepDir
            step_counts+=1
            print(step_counts)
            time.sleep(self.__wait_time)     # Wait before moving on
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
            self.__listen_monitor.run()
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

    #Frequencies
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
        Monitor(self.name +" Sound Monitor",self.sound_change,self.sound_detect_interval).run()
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
            self.__listen_monitor.run()
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
class MicroServer:
    __control_gpio=None
    
    __duty_cycle_for_stopping = 0
    __duty_cycle_min = 2
    __duty_cycle_max = 12
    
    __min_angle = 0
    __max_angle = 180
    __angle_range = __max_angle-__min_angle
    __current_angle = None
    __full_angle_sweep_time = 0.5 #0.6 #Seconds
    __angular_speed = __full_angle_sweep_time/__angle_range #Degrees per sec
    
    __PWM_frequency = 50 #Hertz
    __PWM_control=None
    
    #duty_cycle_mid = (duty_cycle_end  -duty_cycle_start )/2
    
    time_delay=0.04

    def __init__(self, control_gpio):
        self.__control_gpio = control_gpio
        GPIO.setup(control_gpio, GPIO.OUT)
        self.__PWM_control = GPIO.PWM(control_gpio, self.__PWM_frequency) # GPIO 17 for PWM with 50Hz
        self.__PWM_control.start(self.__duty_cycle_for_stopping) # Initialization
    def set_mid(self):
        self.set_angle((self.__min_angle+self.__max_angle)/2)
    def set_angle(self,angle):
        if(self.__current_angle is None):
            time_to_angle = self.__full_angle_sweep_time
        else:
            time_to_angle = abs(self.__current_angle- angle)*self.__angular_speed
        angle_ratio = angle/self.__angle_range
        angle_addition_to_duty_cycle = angle_ratio*(self.__duty_cycle_max - self.__duty_cycle_min)
        new_duty_cycle =  self.__duty_cycle_min+angle_addition_to_duty_cycle
        self.__PWM_control.ChangeDutyCycle(new_duty_cycle)
        time.sleep(time_to_angle)
        self.__current_angle = angle
        self.stop_servo()
    def stop_servo(self):
        self.__PWM_control.ChangeDutyCycle(self.__duty_cycle_for_stopping)
    def get_angle(self):
        return self.__current_angle

        
__init_board()
