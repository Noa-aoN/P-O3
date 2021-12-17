from time import sleep
import RPi.GPIO as GPIO
def setup():
    Motor1A = 24
    Motor1B = 23
    Motor1E = 25
    GPIO.setmode(GPIO.BCM)  # GPIO Numbering
    GPIO.setup(Motor1A, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)

def dcmotor_rotate():
    Motor1A = 24
    Motor1B = 23
    Motor1E = 25
    GPIO.setmode(GPIO.BCM)  # GPIO Numbering
    GPIO.setup(Motor1A, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)

    # Going forwards
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(.20)
    # Stop
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.cleanup()

def servo_rotate(player):
    servoPIN = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    pos1 = 300 + (player) * (1020 - 300) / 3
    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(2.5)  # Initialization
    p.ChangeDutyCycle(int(pos1 / 100))
    sleep(1)
    p.stop()
    GPIO.cleanup()

def servo_rotate_fromto(previous_player,player):
    servoPIN = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    pos0 = 300 + (previous_player)*(1020-300)/3
    pos1 = 300 + (player) * (1020 - 300) / 3
    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(2.5)  # Initialization
    if int(pos0)<int(pos1):
        for i in range(int(pos0), int(pos1)):
            p.ChangeDutyCycle(i / 100)
            sleep(0.005)
    elif int(pos0)>int(pos1):
        for i in range(int(pos0), int(pos1),-1):
            p.ChangeDutyCycle(i / 100)
            sleep(0.005)
    p.stop()
    GPIO.cleanup()