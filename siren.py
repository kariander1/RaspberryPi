import RPi.GPIO as GPIO
import time


class MorseLetter:
  def __init__(self, letterCharacter, sequence):
      self.character = letterCharacter
      self.sequence=sequence
      self.unicode = ord(letterCharacter)

#    dictionaryName
dictionary=[]
def AddMorseLetter(character):
    dictionary.append(character)
 #   def GetMorseLetterByCharacter(character):
        
class MorsePlayer:
  unitTimeStep = 1 #Seconds
  dotModifier = 1
  dashModifier = 3
  interGapModifier = 1
  letterGapModifier = 3
  wordGapModifier = 7
  switchToUse = 18
  #dictionary
  def __init__(self, dictionary):
      self.dictionary = dictionary
  def playMorseLetter(self, letter)
  
  def playMorseCharacter(self,character):
      for ins in character.sequence:
        if ins=='.':
              openSwitch(self.switchToUse,self.unitTimeStep*self.dotModifier)
        elif ins == '-':
              openSwitch(self.switchToUse,self.unitTimeStep*self.dashModifier)
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
	GPIO.setup(switchnum,GPIO.OUT)
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
gpioInUses =[18]

closeSwitches(gpioInUses)

a = MorseLetter('A',".-")
AddMorseLetter(a)

mp = MorsePlayer(dictionary)
mp.playMorseCharacter(a)

GPIO.cleanup()
