from gpiozero import RGBLED
from time import sleep
import colorsys

led = RGBLED(red=21, green=20, blue=16)

#led.color=(0.1, 0.9, 0.5)
 
#while(True):
for hue in range(101):
    # https://docs.python.org/2/library/colorsys.html
    (r, g, b) = colorsys.hsv_to_rgb(hue/100, 1.0, 1.0)
    #R, G, B = int(255 * r), int(255 * g), int(255 * b)
    led.color=(r,g,b)
    sleep(0.01)
led.close
#for red in range(256) :
#    for green in range(25) :
 #       for blue in range(256) :
  #          led.color=(red/256, green/256, blue/256)
   #         sleep(0.01)
        
    
