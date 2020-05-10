import deviceManager
from time import sleep
import time
from gpiozero import DistanceSensor
import ledMeter
import RPi.GPIO as GPIO



servo_azimuth = deviceManager.init_servo(13,30,4,"Azimuth Servo")
servo_elevation = deviceManager.init_servo(26,6,2,"Elevation Servo")
dis =deviceManager.init_distance_sensor(12,16) 
led_meter = ledMeter.ledMeter()
led_meter.add_led_pin(22)
led_meter.add_led_pin(27)
led_meter.add_led_pin(4)
led_meter.add_led_pin(18)
led_meter.add_led_pin(23)


        
        
servo_elevation.set_mid()

measurement_time = 0.03 # Sec
min_measure = 2000 #cm

angle_interval = 1
angle_start = 0
angle_end = 180
el_interval =3
el_start = 44
el_end = 135
deviceManager.print_gpio_board()

for j in range(el_start,el_end,el_interval):
    servo_elevation.set_angle(j)
    for i in range(angle_start,angle_end+angle_interval,angle_interval):
        servo_azimuth.set_angle(i)
        
        current_measure =dis.take_measurements(measurement_time)
        #current_measure =dis.take_measurement(measurement_time);
        if(current_measure is None):
            #print("Invalid measurement")
            
            None
        else:
            led_meter.set_value(current_measure)
            if( current_measure < min_measure):
                min_measure = current_measure
                min_measure_az = servo_azimuth.get_angle()
                min_measure_el = servo_elevation.get_angle()
                print("New min measure: ",min_measure)
        
    temp = angle_start
    angle_start = angle_end
    angle_end=temp
    angle_interval*=-1

servo_azimuth.set_angle(min_measure_az)
servo_elevation.set_angle(min_measure_el)
text = input()
servo_azimuth.set_mid()
servo_elevation.set_angle(0);