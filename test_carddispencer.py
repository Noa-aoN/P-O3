from carddispencer_functies import setup, dcmotor_rotate, servo_rotate
from time import sleep
servo = Servo(4)

setup()
for i in range(1,5):
    servo_rotate(i)
    dcmotor_rotate(i)
    sleep(10)
