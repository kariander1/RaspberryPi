import deviceManager
from time import sleep
from gpiozero import DistanceSensor
import random
servo_azimuth = deviceManager.init_servo(13,30,4,"Azimuth Servo")
servo_elevation = deviceManager.init_servo(26,6,2,"Elevation Servo")
servo_elevation.mid()
dis = DistanceSensor(12,16,10,3)
val =-1.0
val_dif=0.01
while True:
        
        servo_azimuth.value = val
        print('Distance to nearest object is', dis.distance, 'm')
        val=val+val_dif
        if(val>=1.0):
            val=1.0
            val_dif*=-1
        if(val<=-1.0):
            val=-1.0
            val_dif*=-1
        sleep(0.1)
        
   # servo_azimuth.min()
    #servo_elevation.min()
   # sleep(1)
  #  servo_azimuth.mid()
   
   # sleep(1)
   # servo_azimuth.max()
   # servo_elevation.max()
    #sleep(1)
