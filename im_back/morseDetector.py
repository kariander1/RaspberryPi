import deviceManager
from morse import MorsePlayer
from morse import MorseListener
from time import sleep

led = deviceManager.init_led(27)


devices=[led] #RGB led + led

mp = MorsePlayer(False,devices)

ml = MorseListener()
ml.add_input_light_device(14,6,4)
#print("Please enter morse input")

file = open('im_back/morse Detector/text.txt',mode='r')
 

text = file.read()
ml.start_listening()
mp.playMorseLine(text)
sleep(1)
print("")
deviceManager.exit_program()

