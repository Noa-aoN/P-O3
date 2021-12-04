import cv2
import mediapipe as mp
import time
from Camera import init_camera

"""
kan een heleboel gebaren herkennen via het vergelijken van de coordinaten van de 'landmarks'
er kunnen nog meer gebaren geimplementeerd worden
zelfde programma als 'gestures_mediapipe.py' maar dan in een klasse
link: 
https://optisol.com.au/insight/alphabet-hand-gestures-recognition-using-mediapipe/#:~:text=MediaPipe%20Hand%20is%20a%20machine%20learning%20employed%20high-fidelity,help%20of%20multiple%20models%20which%20are%20working%20simultaneously.
"""
FINGERS = ("Higher / One", "Two", "Three", "Four", "Five")
OPTIONS = ("Hit", "Double Down", "Stand")


def hand_position(hand_landmarks):
    return (hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y, hand_landmarks.landmark[12].x,
            hand_landmarks.landmark[12].y)


def index_down(hand_landmarks):
    if hand_landmarks.landmark[8].y > hand_landmarks.landmark[7].y > hand_landmarks.landmark[6].y > \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y:
        print("lower")
        return True
    return False


def thumbs_up(hand_landmarks):
    if hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y < hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[9].y > hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[13].y > hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[17].y > hand_landmarks.landmark[2].y:
        print("thumbs up")
        return True
    return False


def thumbs_down(hand_landmarks):
    if hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y > hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[9].y < hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[13].y < hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[17].y < hand_landmarks.landmark[2].y:
        print("thumbs down")
        return True
    return False


def index_up(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y > hand_landmarks.landmark[11].y > hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y > hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        print("higher/one")
        return True
    return False


def fingers_two(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y > hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        print("two")
        return True
    return False


def fingers_three(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        print("three")
        return True
    return False


def fingers_five(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y and \
            not ((hand_landmarks.landmark[5].x < hand_landmarks.landmark[4].x < hand_landmarks.landmark[17].x) or
                 (hand_landmarks.landmark[17].x < hand_landmarks.landmark[4].x < hand_landmarks.landmark[5].x)):
        print("five")
        return True
    return False


def fingers_four(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y and \
            ((hand_landmarks.landmark[5].x < hand_landmarks.landmark[4].x < hand_landmarks.landmark[17].x) or
             (hand_landmarks.landmark[17].x < hand_landmarks.landmark[4].x < hand_landmarks.landmark[5].x)):
        # kijken of duim tussen wijsvinger en pink zit (x-coordinaat)
        print("four")
        return True
    return False


def check_all_fingers(handlandmarks):
    finger_functions = [index_up, fingers_two, fingers_three, fingers_four, fingers_five]

    for i, finger_func in enumerate(finger_functions):
        if finger_func(handlandmarks):
            return i + 1, FINGERS[i]

    return None, "No Bet Found"

def check_option(handlandmarks, double_down):
    option_function = [index_up, fingers_two, fingers_five]
    if not double_down:
        option_function.pop(1)

    for i, option_func in enumerate(option_function):
        if option_func(handlandmarks):
            return OPTIONS[i]

    return None


class LandmarkGetter:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands()

    def __call__(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(img)
        landmarklist = []
        if result.multi_hand_landmarks is not None:
            for hand_landmarks in result.multi_hand_landmarks:
                landmarklist.append(hand_landmarks)
        return landmarklist


# om programma te runnen:
# from gestures_mediapipe.py import gesture_recognition
if __name__ == "__main__":
    print("gesture recognition")
