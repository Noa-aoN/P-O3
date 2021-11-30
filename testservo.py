import RPi.GPIO as GPIO
import time

servoPIN = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
#3
#10.1
try:
  while True:
      p.ChangeDutyCycle(3)
      time.sleep(2)
      for i in range(300,1020):
          p.ChangeDutyCycle(i/100)
          print(i)
          time.sleep(0.005)
 
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()