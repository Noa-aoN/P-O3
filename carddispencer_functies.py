from gpiozero import Servo
from time import sleep
import RPi.GPIO as GPIO
servo = Servo(4)


def setup():
    Motor1A = 24
    Motor1B = 23
    Motor1E = 22
    GPIO.setmode(GPIO.BCM)  # GPIO Numbering
    GPIO.setup(Motor1A, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)

def dcmotor_rotate(amount_of_cards):
    # Going forwards
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(1*amount_of_cards)
    # Stop
    GPIO.output(Motor1E, GPIO.LOW)

def servo_rotate(player):
    degree = 180*(player-1)/3
    p = (degree/180) -0.5
    servo.value = p
