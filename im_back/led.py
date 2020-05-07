from gpiozero import LED, Button,PWMLED
from time import sleep

led = PWMLED(27)
button = Button(20)

#while True:
 #   if button.is_pressed:
  #      led.toggle()
bright_val =0
bright_interval =0.01
sleep_interval = 0.01
while True:
    
    
    led.value = bright_val  # off
    bright_val+=bright_interval
    if(bright_val>=1):
    
        bright_interval*=-1
        bright_val=1   
    
    elif(bright_val<=0) :
    
        bright_interval*=-1
        bright_val=0   
    
    sleep(sleep_interval)
    