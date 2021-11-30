from time import sleep
import RPi.GPIO as GPIO
def setup():
    Motor1A = 24
    Motor1B = 23
    Motor1E = 22
    GPIO.setmode(GPIO.BCM)  # GPIO Numbering
    GPIO.setup(Motor1A, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)

def dcmotor_rotate():
    # Going forwards
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(1)
    # Stop
    GPIO.output(Motor1E, GPIO.LOW)

def servo_rotate(player):
    servoPIN = 11
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    pos1 = 300 + (player - 1) * (1020 - 300) / 3
    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(2.5)  # Initialization
    p.ChangeDutyCycle(pos1 / 100)
    p.stop()
    GPIO.cleanup()

def servo_rotate_fromto(previous_player,player):
    servoPIN = 11
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    pos0 = 300 + (previous_player-1)*(1020-300)/3
    pos1 = 300 + (player - 1) * (1020 - 300) / 3
    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(2.5)  # Initialization
    if previous_player < 1:
        p.ChangeDutyCycle(pos1/100)

    for i in range(pos0, pos1):
        p.ChangeDutyCycle(i / 100)
        print(i)
        time.sleep(0.005)
    p.stop()
    GPIO.cleanup()

