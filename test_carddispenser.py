from carddispencer_functies import setup, dcmotor_rotate, servo_rotate , servo_rotate_fromto
from time import sleep
import RPi.GPIO as GPIO
GPIO.cleanup()
for i in range(1,5):
    print(i)
    if i == 1:
        
        servo_rotate(i)
        sleep(1)
        dcmotor_rotate()
    else:
        servo_rotate_fromto(i-1,i)
        sleep(1)
        dcmotor_rotate()
    sleep(5)