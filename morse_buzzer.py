import RPi.GPIO as GPIO
import time
import sys
import threading
from gpiozero import Buzzer

class MorseLetter:
  def __init__(self, letter_character, sequence):
      self.character = letter_character
      self.sequence=sequence
      self.unicode = ord(letter_character)

class MorseDictionary:
    characters=[]
    def __init__(self, dictionary_name):
        self.dictionaryName = dictionary_name
    def add_morse_letter(self, character):
        self.characters.append(character)
    def get_morse_character_by_letter(self, letter):
        for morseLetter in self.characters:
            if ord(letter) == morseLetter.unicode:
                return morseLetter

class MorsePlayer:
  unitTimeStep = 0.1 #Seconds
  dotModifier = 1
  dashModifier = 3
  interGapModifier = 1
  letterGapModifier = 3
  wordGapModifier = 7
  switchesToUse = []
  #dictionary
  def __init__(self, dictionary,switches):
      self.dictionary = dictionary
      self.switchesToUse = switches
  def playMorseLine(self, line):
      for word in line.split():
          self.playMorseWord(word)
          time.sleep(self.unitTimeStep*self.wordGapModifier) 
          print(" ",end ="")
          
  def playMorseWord(self, word):
      for letter in word:
          self.playMorseLetter(letter)
          time.sleep(self.unitTimeStep*self.letterGapModifier)       
          
  def playMorseLetter(self, letter):
      morseChar = self.dictionary.get_morse_character_by_letter(letter.upper())
      print(morseChar.character,end ="")
      sys.stdout.flush()
      self.playMorseCharacter(morseChar)
      
      
  def playMorseCharacter(self,character):
      for ins in character.sequence:
        if ins=='.':
            temp_mod =self.dotModifier 
        elif ins == '-':
            temp_mod = self.dashModifier
            
        for switch in self.switchesToUse:
            set_switch_on(switch)
            
        time.sleep(self.unitTimeStep*temp_mod)
        
        for switch in self.switchesToUse:
            set_switch_off(switch)
        
        time.sleep(self.unitTimeStep*self.interGapModifier)

 # def playMorseWord(word):
#      for character in word:
          
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
    GPIO.setmode(GPIO.BCM)
    for switch in input_pins:
        GPIO.setup(switch, GPIO.IN)
    for switch in output_pins:
        GPIO.setup(switch, GPIO.OUT)

class SoundDetector:
    sound_detect_interval = 100
    def __init__(self, SoundDetector_name, input_switch):
        print ("Initializing "+ SoundDetector_name)
        self.name = SoundDetector_name
        self.detectedSound=False
        self.input_switch = input_switch
        self.output_switches = list()
        GPIO.add_event_detect(input_switch, GPIO.BOTH, bouncetime=self.sound_detect_interval)  # let us know when the pin goes HIGH or LOW
        GPIO.add_event_callback(input_switch, self.sound_change)  # assign function to GPIO PIN, Run function on change
        #Monitor(self.name +" Sound Monitor",self.sound_change,self.sound_detect_interval).start()
        # Add triggers
        print ("Initializing "+ SoundDetector_name+" Done")
    def add_trigger_pin(self,pin_number):
        self.output_switches.append(pin_number)
        
    def sound_change(self,sw):
        print(GPIO.input(self.input_switch))
        #print(self.detectedSound)
        if bool(GPIO.input(self.input_switch)) is self.detectedSound:
            if not GPIO.input(self.input_switch):
                print("Sound Detected!")
                self.detectedSound=True
            else:
                print("Sound Stopped!")
                self.detectedSound=False
                
class Button:
    check_button_interval_ms = 20
    trigger_interval_ms = 20
    def __init__(self, button_name, input_switch):
        print ("Initializing Button "+ button_name)
        self.is_pressed = False
        self.last_is_pressed = False
        self.name = button_name
        self.input_switch = input_switch
        self.output_switches = list()
        Monitor(self.name +" Press Monitor",self.check_button_pressed,self.check_button_interval_ms).start()
        Monitor(self.name +" Trigger Monitor",self.trigger,self.trigger_interval_ms).start()
        print ("Initializing Button "+ button_name+" Done")
    def add_trigger_pin(self,pin_number):
        self.output_switches.append(pin_number)
    def trigger(self):
        #threading.Timer(self.trigger_interval_ms / 1000, self.trigger).start()
        if self.is_pressed is not self.last_is_pressed: #If state was changed
            # print("Toggle")
            # toggleSwitch(switch_to_toggle)
            if self.is_pressed:
                open_switches(self.output_switches)
            else:
                close_switches(self.output_switches)
            self.last_is_pressed = self.is_pressed

    def check_button_pressed(self):
        #threading.Timer(self.check_button_interval_ms/1000, self.check_button_pressed).start()
        input_state = GPIO.input(self.input_switch)  # false means button is pressed
        self.is_pressed = not input_state
        #print("Check Button "+str(self.is_pressed))



class Monitor(threading.Thread):
    global monitors
    
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    interation = 0    
    method_running = False
    def __init__(self,monitor_name,method_to_execute,rate_ms, *args, **kwargs):
        super(Monitor, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
        self.method_to_execute = method_to_execute
        self.rate_ms = rate_ms
        self.monitor_name = monitor_name
        monitors.append(self)
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    
    def run(self):
        #self.interation = self.interation+1
        if(self.stopped()):
            return
        th = threading.Timer(self.rate_ms/1000, self.run)
        th.start()
        
        if self.method_running :
            print(self.monitor_name+ " Previous run not finished ")#+str(self.interation))
            return
        self.method_running = True
        self.last_thread = th
        self.method_to_execute()
        self.method_running = False
        
    def join(self, timeout=None):
        """ Stop the thread and wait for it to end. """
        print(self.monitor_name+ ' exiting thread')
        self._stop.set( )
        self.last_thread.join()
        monitors.remove(self)
        print(self.monitor_name+ ' exiting thread successfully')
    def __del__(self):
        self.join()
    def __exit__(self):
        self.join()

            
def exit_program():
    print("Exiting program..")
    print("Threads alive : " +str(threading.active_count()))
    temp_monitors = monitors.copy()
    for monitor in temp_monitors:
            monitor.join()
    GPIO.cleanup()
    print("Exit Done")




monitors = list()
input_pins =[20,26]
output_pins =[4, 17, 18, 27, 22]
initialize_board(input_pins,output_pins)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.add_event_detect(26, GPIO.BOTH, bouncetime=100)  # let us know when the pin goes HIGH or LOW
#GPIO.add_event_callback(26, sound_change)  # assign function to GPIO PIN, Run function on change
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_UP)
sd = SoundDetector("Morse Detector",26)

button_a = Button("Buzzer",20)
button_a.add_trigger_pin(17)

#buta = threading.Thread(target=printit)
#but = Monitor("Button",printit,1000)
#but.start()

#printit()
intDic = MorseDictionary("International")
#a = MorseLetter('A',".-")
#intDic.add_morse_letter(a)

file = open("international.mrs", "r")
for line in file: 
  temp = line.split()
  intDic.add_morse_letter(MorseLetter(temp[0], temp[1]))
    
mp = MorsePlayer(intDic, output_pins)

print("Please enter morse input")
text = input()
mp.playMorseLine(text)


exit_program()

