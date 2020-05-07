import deviceManager
import time
import sys
import gpio
import threading
from enum import Enum
from gpiozero import Buzzer
from gpiozero import LED
from monitor import Monitor

DOT='.'
DASH='-'
class MorseLetter:
    def __init__(self, letter_character, sequence):
        self.character = letter_character
        self.sequence=sequence
        self.unicode = ord(letter_character)
    def __str__(self):
        return '('+self.unicode+')'+self.character+' '+self.sequence
    def __repr__(self):
        return self.__str__
class MorseDictionary:
    #Defaults
    unit_time_step = 0.05 #Seconds
    dot_time_modifier = 1
    dash_time_modifier = 3
    character_gap_modifier = 1
    letter_gap_modifier = 3
    word_gap_modifier = 7
    default_dictionary= """
    A	.-
    B	-...
    C	-.-.
    D	-..
    E	.
    F	..-.
    G	--.
    H	....
    I	..
    J	.---
    K	-.-
    L	.-..
    M	--
    N	-.
    O	---
    P	.--.
    Q	--.-
    R	.-.
    S	...
    T	-
    U	..-
    V	...-
    W	.--
    X	-..-
    Y	-.--
    Z	--..
    0	-----
    1	.----
    2	..---
    3	...--
    4	....-
    5	.....
    6	-....
    7	--...
    8	---..
    9	----.
    &	.-...
    '	.----.
    @	.--.-.
    )	-.--.-
    (	-.--.
    :	---...
    ,	--..--
    =	-...-
    !	-.-.--
    .	.-.-.-
    -	-....-
    +	.-.-.
    "	.-..-.
    ?	..--..
    /	-..-.
    ;   -.-.-.
    """
    special_characters = {
    "AA": '\n',
    "BK": "\t",
    }
    
    characters=[]
    def __init__(self, dictionary_name,path_to_morse_file=None):
        self.dictionaryName = dictionary_name
        self.__load_dictionary(path_to_morse_file)
        
    def __load_dictionary(self,path_to_morse_file=None):
        self.characters=[]
        if path_to_morse_file==None:
            file = self.default_dictionary.split('\n')
        else :
            file = open(path_to_morse_file, "r")
        for line in file: 
            line_elements = line.split()
            if len(line_elements)>1:
                self.__add_morse_letter(MorseLetter(line_elements[0], line_elements[1]))
        self.__load_special_characters()
        
    def __load_special_characters(self):
        for special in self.special_characters:
            temp_seq=""
            for letter in special:
                temp_seq+=(self.get_morse_character_by_letter(letter).sequence)
            self.__add_morse_letter(MorseLetter(self.special_characters[special],temp_seq))
       
    def __add_morse_letter(self, character):
        self.characters.append(character)
    def get_morse_character_by_letter(self, letter):
        for morseLetter in self.characters:
            if ord(letter) == morseLetter.unicode:
                return morseLetter
        return ""
    def get_morse_letter_by_sequence(self, sequence):
        if sequence is "":
            return ""
        for morseLetter in self.characters:
            if morseLetter.sequence == sequence:
                return morseLetter.character
        return "�"
            
    def get_morse_character_play_time(self,character):
        temp_mod=0
        if character==DOT:
            temp_mod =self.dot_time_modifier 
        elif character == DASH:
            temp_mod = self.dash_time_modifier
        return temp_mod*self.unit_time_step
    def __str__(self):
        return self.dictionaryName
    __temp_sequence=""
    def parse_measures(self,measures):
        parsed_text=""
        while len(measures) > 0:
            lightMeasure = measures.pop(0)
       # for lightMeasure in measures:
            if(lightMeasure.turned_on):
                self.__temp_sequence+=self.__parse_on_measure(lightMeasure.duration)
            else:#Finished sequence
                off_punctuation = self.__parse_off_measure(lightMeasure.duration)
                if(off_punctuation is not OffPunctuation.CHAR_GAP):
                    parsed_text+=self.get_morse_letter_by_sequence(self.__temp_sequence)
                    self.__temp_sequence=""                    
                    if(off_punctuation == OffPunctuation.WORD_GAP):
                        parsed_text+=" "
        return parsed_text
    def __parse_on_measure(self,duration):
        delta_from_dot =abs(duration-self.unit_time_step*self.dot_time_modifier)
        delta_from_dash =abs(duration-self.unit_time_step*self.dash_time_modifier)
        if(delta_from_dot<delta_from_dash):
            return DOT
        else:
            return DASH
    def __parse_off_measure(self,duration):
        delta_from_char_gap =abs(duration-self.unit_time_step*self.character_gap_modifier)
        delta_from_letter_gap =abs(duration-self.unit_time_step*self.letter_gap_modifier)
        delta_from_word_gap =abs(duration-self.unit_time_step*self.word_gap_modifier)
        min_delta = min(delta_from_char_gap,delta_from_letter_gap,delta_from_word_gap)
        
        if(min_delta == delta_from_char_gap):
            return OffPunctuation.CHAR_GAP
        if(min_delta == delta_from_letter_gap):
            return OffPunctuation.LETTER_GAP
        if(min_delta == delta_from_word_gap):
            return OffPunctuation.WORD_GAP
class OffPunctuation(Enum):
    CHAR_GAP = 1
    LETTER_GAP = 2
    WORD_GAP = 3
class MorseListener:
    __is_listening=False
    __listen_inteval=100
    def __init__(self ,dictionary_name="International Morse",path_to_morse_file=None):
        self.define_dictionary_path_name(dictionary_name,path_to_morse_file)
        self.__listen_inteval = 1000*self.__dictionary.unit_time_step*self.__dictionary.dot_time_modifier
        self.__listen_monitor = Monitor("Morse Monitor",self.__listen_for_measurements,self.__listen_inteval)
        self.__devices=[]
    def start_listening(self):
        self.__is_listening =True
        self.__listen_monitor.start()
        for device in self.__devices:
            device.start_listening()
        
    def __listen_for_measurements(self):
        for device in self.__devices:
            print(self.__dictionary.parse_measures(device.morse_measurements),end = '')
    def add_input_light_device(self,gpio_pin,gnd_pin=-1,vcc_pin=-1):
        light_detector = deviceManager.init_light_detector(gpio_pin,gnd_pin,vcc_pin,"Morse Light Detector")
        light_detector.set_detect_interval(1000*self.__dictionary.unit_time_step*self.__dictionary.dot_time_modifier/2)
        self.__devices.append(light_detector)
        return light_detector
    def remove_input_device(self,device):
        self.__devices.remove(device)
    def define_dictionary_path_name(self,dictionary_name="International Morse",path_to_morse_file=None):
            self.__dictionary = MorseDictionary(dictionary_name,path_to_morse_file)
            

    def define_dictionary(self,dictionary):
            self.__dictionary = dictionary
            
         
class MorsePlayer:
    #dictionary
    def __init__(self ,show_output=False,devices=None,dictionary_name="International Morse",path_to_morse_file=None):
        self.define_dictionary_path_name(dictionary_name,path_to_morse_file)
        self.__devices=[]
        self.show_output = show_output
        if devices!=None:
            self.__devices=devices
        # self.devices = devices
    def define_dictionary_path_name(self,dictionary_name="International Morse",path_to_morse_file=None):
            self.__dictionary = MorseDictionary(dictionary_name,path_to_morse_file)
            self.__calc_dictionary_properties()

    def define_dictionary(self,dictionary):
            self.__dictionary = dictionary
            self.__calc_dictionary_properties()
            
    def __calc_dictionary_properties(self):
        self.__word_gap_time_step = ((self.__dictionary.unit_time_step)*(self.__dictionary.word_gap_modifier))
        self.__letter_gap_time_step =(self.__dictionary.unit_time_step*self.__dictionary.letter_gap_modifier)
        self.__chracter_gap_time_step =(self.__dictionary.unit_time_step*self.__dictionary.character_gap_modifier)
        
        
    def playMorseLine(self, line):
        for word in line.split(' '):
            self.__playMorseWord(word)
            time.sleep(self.__word_gap_time_step)
            if self.show_output is True:
                print(" ",end ="")
            
    def add_output_device(self,device):
        self.__devices.append(device)
        
    def remove_output_device(self,device):
        self.__devices.remove(device)
        
    def __playMorseWord(self, word):
        for letter in word:
            self.__playMorseLetter(letter)
            time.sleep(self.__letter_gap_time_step)       
            
    def __playMorseLetter(self, letter):
        morseChar = self.__dictionary.get_morse_character_by_letter(letter.upper())
        if morseChar is not "":
            if self.show_output is True:
                print(morseChar.character,end ="")
            sys.stdout.flush()
            self.__playMorseCharacter(morseChar)
        
    def __playMorseCharacter(self,character):
        for ch in character.sequence:
            play_time =self.__dictionary.get_morse_character_play_time(ch)
                
            self.__change_devices_status(True) # Turn on LEDS/Buzzers
            time.sleep(play_time)
            
            self.__change_devices_status(False)# Turn off LEDS/Buzzers
            
            time.sleep(self.__chracter_gap_time_step)
            
    def __handle_led_status(self,led,turn_on):
        if turn_on:
            led.on()
        else:
            led.off()
            
    def __handle_buzzer_status(self,buzzer,turn_on):
        if turn_on:
            buzzer.on()
        else:
            buzzer.off()
            
    def __handle_unknown_device_status(self,device,turn_on):#Treats unknown devices as pins need to be opened
        if turn_on:
            gpio.set_switch_on(device)
        else:
            gpio.set_switch_off(device)
            
    def __change_devices_status(self,turn_on=True):
        for device in self.__devices:
                if isinstance(device,LED):                
                    self.__handle_led_status(device,turn_on)
                elif isinstance(device,Buzzer):
                    self.__handle_buzzer_status(device,turn_on)
                else: self.__handle_unknown_device_status(device,turn_on)
                    
    



