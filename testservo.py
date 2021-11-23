from gpiozero import Servo
from time import sleep

servo = Servo(4)
# if playerturn(playername) == True and playerface(playername)==playername
# servo dont move
# if not
# servo moves to designated position
# if playername is fourth player
# turn all the way to the beninging
try:
    while True:
        servo.min()
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)
except KeyboardInterrupt:
    print("Program stopped")