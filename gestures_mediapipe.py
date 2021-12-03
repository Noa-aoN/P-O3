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


# def draw_thumb(img, hand_landmarks, width, height):  # draw functions not used in final version
#     cv2.line(img, (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
#              (int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
#              (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
#              (0, 255, 0), thickness=1)
#
#
# def draw_index(img, hand_landmarks, width, height):
#     cv2.line(img, (int(hand_landmarks.landmark[7].x * width), int(hand_landmarks.landmark[7].y * height)),
#              (int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height)),
#              (int(hand_landmarks.landmark[7].x * width), int(hand_landmarks.landmark[7].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)),
#              (int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height)),
#              (0, 255, 0), thickness=1)
#
#
# def draw_middle(img, hand_landmarks, width, height):
#     cv2.line(img, (int(hand_landmarks.landmark[11].x * width), int(hand_landmarks.landmark[11].y * height)),
#              (int(hand_landmarks.landmark[12].x * width), int(hand_landmarks.landmark[12].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height)),
#              (int(hand_landmarks.landmark[11].x * width), int(hand_landmarks.landmark[11].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)),
#              (int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height)),
#              (0, 255, 0), thickness=1)
#
#
# def draw_ring(img, hand_landmarks, width, height):
#     cv2.line(img, (int(hand_landmarks.landmark[15].x * width), int(hand_landmarks.landmark[15].y * height)),
#              (int(hand_landmarks.landmark[16].x * width), int(hand_landmarks.landmark[16].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height)),
#              (int(hand_landmarks.landmark[15].x * width), int(hand_landmarks.landmark[15].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height)),
#              (int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)),
#              (0, 255, 0), thickness=1)
#
#
# def draw_pinky(img, hand_landmarks, width, height):
#     cv2.line(img, (int(hand_landmarks.landmark[19].x * width), int(hand_landmarks.landmark[19].y * height)),
#              (int(hand_landmarks.landmark[20].x * width), int(hand_landmarks.landmark[20].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height)),
#              (int(hand_landmarks.landmark[19].x * width), int(hand_landmarks.landmark[19].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)),
#              (int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height)),
#              (0, 255, 0), thickness=1)
#
#
# def draw_palm(img, hand_landmarks, width, height):
#     cv2.line(img, (int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)),
#              (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)),
#              (int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)),
#              (int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
#              (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
#              (int(hand_landmarks.landmark[1].x * width), int(hand_landmarks.landmark[1].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[0].x * width), int(hand_landmarks.landmark[0].y * height)),
#              (int(hand_landmarks.landmark[1].x * width), int(hand_landmarks.landmark[1].y * height)),
#              (0, 255, 0), thickness=1)
#     cv2.line(img, (int(hand_landmarks.landmark[0].x * width), int(hand_landmarks.landmark[0].y * height)),
#              (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)),
#              (0, 255, 0), thickness=1)
#
#
# def draw_hand(img, hand_landmarks, width, height):
#     draw_thumb(img, hand_landmarks, width, height)
#     draw_index(img, hand_landmarks, width, height)
#     draw_middle(img, hand_landmarks, width, height)
#     draw_ring(img, hand_landmarks, width, height)
#     draw_pinky(img, hand_landmarks, width, height)
#     draw_palm(img, hand_landmarks, width, height)


def get_landmarks(frame):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    landmarklist = []
    if result.multi_hand_landmarks is not None:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarklist.append(hand_landmarks)
    return landmarklist


# def recognition():
#     cap = init_camera(0)
#     mp_hands = mp.solutions.hands
#     hands = mp_hands.Hands()
#
#     if cap.isOpened():
#         # while cap.isOpened():  # main loop
#         ret, frame = cap.read()
#
#         img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         result = hands.process(img)
#         img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # opencv gebruikt bgr!
#         if result.multi_hand_landmarks is not None:
#             for hand_landmarks in result.multi_hand_landmarks:
#                 for point in range(21):  # 0-20
#                     height, width, _ = frame.shape
#                     pointcoords = hand_landmarks.landmark[point]
#                     x = int(pointcoords.x * width)  # x en y zijn genormaliseerd dus geeft het percentage aan
#                     # (als de foto 60 pixels breed is en x = 0.20, spreekt hij over xpixel 12)
#                     y = int(pointcoords.y * height)
#                     # cv2.line(img, (points[0]), (points[1]), (0, 255, 0), thickness=3, lineType=8)
#                     cv2.circle(img, (x, y), 2, (0, 0, 255))
#
#                 """
#                 Drawing the hands by connecting dots
#                 """
#                 # .hand_position(hand_landmarks) # positie handpalm weergeven
#                 # .draw_hand(img, hand_landmarks, width, height) # hand tekenen niet nodig voor uiteindelijke herkenning
#
#                 """ Gesture Recognition"""
#
#                 # all recognizable gestures, more can be implemented
#                 # allemaal if's toegevoegd zodat meerdere gebaren niet tegelijk kunnen herkend worden, simpelste gebaren vanboven
#                 if index_down(img, hand_landmarks):
#                     return "index down"
#                 elif thumbs_up(img, hand_landmarks):
#                     return "thumbs up"
#                 elif thumbs_down(img, hand_landmarks):
#                     return "thumbs down"
#                 elif index_up(img, hand_landmarks):
#                     return "index up"
#                 elif fingers_five(img, hand_landmarks):
#                     return "five"
#                 elif fingers_four(img, hand_landmarks):
#                     return "four"
#                 elif fingers_three(img, hand_landmarks):
#                     return "three"
#                 elif fingers_two(img, hand_landmarks):
#                     return "two"
#                     # draw_hand(img, hand_landmarks, width, height)
#                     # index_down(img, hand_landmarks)
#                     # thumbs_up(img, hand_landmarks)
#                     # thumbs_down(img, hand_landmarks)
#                     # index_up(img, hand_landmarks)
#                     # fingers_five(img, hand_landmarks)
#                     # fingers_four(img, hand_landmarks)
#                     # fingers_three(img, hand_landmarks)
#                     # fingers_two(img, hand_landmarks)
#
#             # cv2.imshow('Raw Webcam Feed', img)
#
#             # if cv2.waitKey(10) & 0xFF == ord('q'):  # q om te stoppen
#             #     break
#
#     cap.release()
#     cv2.destroyAllWindows()
#     return None


# om programma te runnen:
# from gestures_mediapipe.py import gesture_recognition
if __name__ == "__main__":
    recognition()
