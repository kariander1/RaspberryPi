import time
import sys
from gpiozero import OutputDevice as stepper
import deviceManager

step = deviceManager.init_stepper_motor(4,27,22,23)

deviceManager.print_gpio_board()
step.rotate(360)
#step.rotate_steps(2048)
"""
IN1 = stepper(4)
IN2 = stepper(27)
IN3 = stepper(22)
IN4 = stepper(23)
stepPins = [IN1,IN2,IN3,IN4] # Motor GPIO pins</p><p>
stepDir = 2        # Set to 1 for clockwise
                           # Set to -1 for anti-clockwise
mode = 1            # mode = 1: Low Speed ==> Higher Power
                           # mode = 0: High Speed ==> Lower Power
if mode:              # Low Speed ==> High Power
  seq = [[1,0,0,1], # Define step sequence as shown in manufacturers datasheet
             [1,0,0,0], 
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1]]
else:                    # High Speed ==> Low Power 
  seq = [[1,0,0,0], # Define step sequence as shown in manufacturers datasheet
             [0,1,0,0],
             [0,0,1,0],
             [0,0,0,1]]
stepCount = len(seq)
if len(sys.argv)>1: # Read wait time from command line
  waitTime = int(sys.argv[1])/float(1000)
else:
  waitTime = 0.004    # 2 miliseconds was the maximun speed got on my tests
stepCounter = 0

step_counts=0
while step_counts<2048:                          # Start main loop
  for pin in range(0,4):
    xPin=stepPins[pin]          # Get GPIO
    if seq[stepCounter][pin]!=0:
      xPin.on()
    else:
      xPin.off()
  stepCounter += stepDir
  if (stepCounter >= stepCount):
    stepCounter = 0
  if (stepCounter < 0):
    stepCounter = stepCount+stepDir
  step_counts+=1
  print(step_counts)
  time.sleep(waitTime)     # Wait before moving on
  
  """