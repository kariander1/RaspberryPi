import RPi.GPIO as GPIO
import time
import sys
from gpiozero import Buzzer

class MorseLetter:
  def __init__(self, letterCharacter, sequence):
      self.character = letterCharacter
      self.sequence=sequence
      self.unicode = ord(letterCharacter)

class MorseDictionary:
    characters=[]
    def __init__(self, dictionaryName):
        self.dictionaryName = dictionaryName
    def AddMorseLetter(self, character):
        self.characters.append(character)
    def GetMorseCharacterByLetter(self,letter):
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
      morseChar = self.dictionary.GetMorseCharacterByLetter(letter.upper())
      print(morseChar.character,end ="")
      sys.stdout.flush()
      self.playMorseCharacter(morseChar)
      
      
  def playMorseCharacter(self,character):
      for ins in character.sequence:
        if ins=='.':
            tempMod =self.dotModifier 
        elif ins == '-':
            tempMod = self.dashModifier
            
        for switch in self.switchesToUse:
            setSwitchOn(switch)
            
        time.sleep(self.unitTimeStep*tempMod)
        
        for switch in self.switchesToUse:
            setSwitchOff(switch)
        
        time.sleep(self.unitTimeStep*self.interGapModifier)

 # def playMorseWord(word):
#      for character in word:
          
def closeSwitches(switches):
    for switch in switches:
        setSwitchOff(switch)
        
def setSwitchOff(switchNum):
	GPIO.setup(switchNum,GPIO.OUT)
	GPIO.output(switchNum,GPIO.LOW)
	
def setSwitchOn(switchNum):
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

GPIO.setmode(GPIO.BCM)
gpioInUses =[4,17,18,27,22]
closeSwitches(gpioInUses)
intDic = MorseDictionary("International")
#a = MorseLetter('A',".-")
#intDic.AddMorseLetter(a)

file = open("international.mrs", "r")
for line in file: 
  temp = line.split()
  intDic.AddMorseLetter(MorseLetter(temp[0],temp[1]))
    
mp = MorsePlayer(intDic,gpioInUses)

print("Please enter morse input")
text = input()
mp.playMorseLine(text)

GPIO.cleanup()
