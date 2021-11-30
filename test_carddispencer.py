from carddispencer_functies import setup, dcmotor_rotate, servo_rotate , servo_rotate_fromto
from time import sleep

setup()
for i in range(1,5):
    if i == 1:
        servo_rotate(i)
        dcmotor_rotate()
    else:
        ervo_rotate_fromto(i-1,i)
        dcmotor_rotate()
    sleep(10)
