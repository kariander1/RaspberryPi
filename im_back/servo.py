import deviceManager
from time import sleep
import time
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO



servo_azimuth = deviceManager.init_servo(13,30,4,"Azimuth Servo")
servo_elevation = deviceManager.init_servo(26,6,2,"Elevation Servo")
dis =deviceManager.init_distance_sensor(12,16) 


        
        
servo_elevation.set_mid()

measurement_time = 0.01 # Sec
min_measure = 2000 #cm

angle_interval = 1
angle_start = 0
angle_end = 180
el_interval =3
for j in range(44,135,el_interval):
    servo_elevation.set_angle(j)
    for i in range(angle_start,angle_end+angle_interval,angle_interval):
        servo_azimuth.set_angle(i)
        current_measure =dis.take_measurements(measurement_time)
        
        if(current_measure is None):
            print("Invalid measurement")
        elif( current_measure < min_measure):
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