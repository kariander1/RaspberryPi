from picamera import PiCamera
from time import sleep


def fade_in(duration_sec):
    val =0
    interval_ms = 10
    intervals = (duration_sec*1000)/(interval_ms)
    diff = 255/intervals
  # camera.start_preview(alpha=int(val))
    while(val<255):
        #print("Alpha is "+str(val))
        camera.preview.alpha = int(val)
        val+=diff
        sleep(interval_ms/1000)
    camera.preview.alpha = 255


def fade_out(duration_sec):
    val =255
    interval_ms = 10
    intervals = (duration_sec*1000)/(interval_ms)
    diff = 255/intervals
    #camera.start_preview(alpha = 255)
    while(val>0):
        #print("Alpha is "+str(val))
        camera.preview.alpha = int(val)
        val-=diff
        sleep(interval_ms/1000)
    camera.preview.alpha = 0
camera = PiCamera()
c = 0
camera.start_preview()
while c<100 :
    
    fade_in(0.1)
    fade_out(0.1)
    c=c+1
    
camera.stop_preview()