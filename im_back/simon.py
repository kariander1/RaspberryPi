import RPi.GPIO as GPIO
import time
import sys
import deviceManager
from deviceManager import Button
import random



wait_for_input=True
chosen_pin=None
chosen_led=None

def indicate_player_turn(devices,led_all_on_time):
    for led in leds:
        led.on()
    time.sleep(led_all_on_time)
    for led in leds:
        led.off()
def get_led_input():
    pot.stop()
    global chosen_pin
    global chosen_led
    chosen_pin =(pot.current_pin_output)
    
    chosen_led = leds[leds_pins.index(chosen_pin)]
    chosen_led.blink(0.1,0.1)

def accept_input():
    global chosen_led
    global wait_for_input
    chosen_led.on()
    wait_for_input=False

def await_input():
    global wait_for_input
    wait_for_input=True
    pot.start()
    while(wait_for_input):
        c=0
def indicate_led(pin,with_sound=True):
    index = leds_pins.index(pin)
    current_led = leds[index]
    buzzer.play_note(freqs[index],on_time*time_modifier)
    current_led.on()
    time.sleep(on_time*time_modifier)
    current_led.off()
    time.sleep(off_time*time_modifier)
    
def calc_level_time_modifier(level):
    return (0.0005*level)**2 - 0.0381*level + 1.0493
button_in = deviceManager.init_button(20,39,"Simon Button")
button_in.when_pressed = get_led_input
button_in.when_released  = accept_input

buzzer = deviceManager.init_music_buzzer(17,9,"Game beeper")

leds_pins = [23,18,4,27,22]
leds=[]
min_freq = 500
max_freq = 700
diff = (max_freq-min_freq)/(len(leds_pins)-1)
freqs =[]
for i in range(len(leds_pins)):
    freqs.append(min_freq+i*diff)

a_pin = 16
b_pin = 12
pot = deviceManager.init_potentiometer(a_pin,b_pin,34,"Light Knob")
for x in leds_pins:
    led = deviceManager.init_led(x)
    leds.append(led)
    pot.add_output_pin(x)
    
    
deviceManager.print_gpio_board()



run_game = True
chosen_led=None
chosen_pin=None
time_modifier=1.0
on_time = 1
off_time = 0.3
led_all_on_time =0.2
levels_delay =1
level = 1
pin_series=[]
while run_game:    
    print("Level ",level)
    time_modifier = calc_level_time_modifier(level)
    for pin in pin_series:
        indicate_led(pin)
        
    led_index =  random.randint(0, len(leds)-1)
    pin_series.append(leds_pins[led_index])
    
    indicate_led(leds_pins[led_index])

    indicate_player_turn(leds,led_all_on_time)
    
    if(pot.current_pin_output!= -1):
        leds[leds_pins.index(pot.current_pin_output)].on()
    for pin in pin_series:
        await_input()
        if(chosen_pin != pin):
            buzzer.play_incorrect()
            leds[leds_pins.index(pin_series[-1])].on()
            run_game=False
            break
       
    if(run_game):
        leds[leds_pins.index(pot.current_pin_output)].off()
        buzzer.play_correct()
        level=level+1
    
    time.sleep(levels_delay)

deviceManager.exit_program()
