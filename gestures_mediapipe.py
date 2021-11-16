import cv2
import mediapipe as mp

"""
functionaliteiten:
- thumbs up 
- higher lower
- counting fingers (max 5)

link: 
https://optisol.com.au/insight/alphabet-hand-gestures-recognition-using-mediapipe/#:~:text=MediaPipe%20Hand%20is%20a%20machine%20learning%20employed%20high-fidelity,help%20of%20multiple%20models%20which%20are%20working%20simultaneously.
"""
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


# mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1)
def pointer_up():
    if hand_landmarks.landmark[8].y > hand_landmarks.landmark[7].y > hand_landmarks.landmark[6].y > \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y:
        cv2.putText(
            img=img,
            text=str("Lower"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


def thumbs_up():
    if hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[9].y > hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[13].y > hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[17].y > hand_landmarks.landmark[2].y:
        cv2.putText(
            img=img,
            text=str("Thumbs Up"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


def thumbs_down():
    if hand_landmarks.landmark[4].y > hand_landmarks.landmark[3].y > \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[9].y < hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[13].y < hand_landmarks.landmark[2].y and \
            hand_landmarks.landmark[17].y < hand_landmarks.landmark[2].y:
        cv2.putText(
            img=img,
            text=str("Thumbs down"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


def finger_higher():
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y > hand_landmarks.landmark[11].y > hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y > hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        cv2.putText(
            img=img,
            text=str("Higher / one"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


def fingers_two():
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y > hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        cv2.putText(
            img=img,
            text=str("Two"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


def fingers_three():
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        cv2.putText(
            img=img,
            text=str("Three"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


def fingers_four():
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y:
        cv2.putText(
            img=img,
            text=str("Four"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


def fingers_five():
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y and \
            abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[17].x) > \
            abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[
                5].x):  # afstand duim en pink vergelijken
        cv2.putText(
            img=img,
            text=str("Five"),
            org=(0, 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
            thickness=1)
        return True
    else:
        return False


# Thumb:
def draw_thumb(img, hand_landmarks, width, height):
    cv2.line(img, (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
             (int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
             (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
             (0, 255, 0), thickness=1)


# IndexFinger:
def draw_indexfinger(img, hand_landmarks, width, height):
    cv2.line(img, (int(hand_landmarks.landmark[7].x * width), int(hand_landmarks.landmark[7].y * height)),
             (int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height)),
             (int(hand_landmarks.landmark[7].x * width), int(hand_landmarks.landmark[7].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)),
             (int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height)),
             (0, 255, 0), thickness=1)


# MiddleFinger:
def draw_middlefinger(img, hand_landmarks, width, height):
    cv2.line(img, (int(hand_landmarks.landmark[11].x * width), int(hand_landmarks.landmark[11].y * height)),
             (int(hand_landmarks.landmark[12].x * width), int(hand_landmarks.landmark[12].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height)),
             (int(hand_landmarks.landmark[11].x * width), int(hand_landmarks.landmark[11].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)),
             (int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height)),
             (0, 255, 0), thickness=1)


# RingFinger:
def draw_ringfinger(img, hand_landmarks, width, height):
    cv2.line(img, (int(hand_landmarks.landmark[15].x * width), int(hand_landmarks.landmark[15].y * height)),
             (int(hand_landmarks.landmark[16].x * width), int(hand_landmarks.landmark[16].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height)),
             (int(hand_landmarks.landmark[15].x * width), int(hand_landmarks.landmark[15].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height)),
             (int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)),
             (0, 255, 0), thickness=1)


# Pinky:
def draw_pinky(img, hand_landmarks, width, height):
    cv2.line(img, (int(hand_landmarks.landmark[19].x * width), int(hand_landmarks.landmark[19].y * height)),
             (int(hand_landmarks.landmark[20].x * width), int(hand_landmarks.landmark[20].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height)),
             (int(hand_landmarks.landmark[19].x * width), int(hand_landmarks.landmark[19].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)),
             (int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height)),
             (0, 255, 0), thickness=1)


# Palm:

def draw_palm(img, hand_landmarks, width, height):
    cv2.line(img, (int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)),
             (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)),
             (int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)),
             (int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
             (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
             (int(hand_landmarks.landmark[1].x * width), int(hand_landmarks.landmark[1].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[0].x * width), int(hand_landmarks.landmark[0].y * height)),
             (int(hand_landmarks.landmark[1].x * width), int(hand_landmarks.landmark[1].y * height)),
             (0, 255, 0), thickness=1)
    cv2.line(img, (int(hand_landmarks.landmark[0].x * width), int(hand_landmarks.landmark[0].y * height)),
             (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)),
             (0, 255, 0), thickness=1)


while cap.isOpened():
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(img)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # opencv gebruikt bgr!
    if result.multi_hand_landmarks is not None:
        for hand_landmarks in result.multi_hand_landmarks:
            for point in range(21):
                height, width, _ = frame.shape
                pointcoords = hand_landmarks.landmark[point]
                x = int(pointcoords.x * width)  # x en y zijn genormaliseerd dus geeft het percentage aan
                # (als de foto 60 pixels breed is en x = 0.20, spreekt hij over xpixel 12)
                y = int(pointcoords.y * height)
                # cv2.line(img, (points[0]), (points[1]), (0, 255, 0), thickness=3, lineType=8)
                cv2.circle(img, (x, y), 2, (0, 0, 255))

            """
            Drawing the hands by connecting dots
            """

            draw_palm(img, hand_landmarks, width, height)
            draw_thumb(img, hand_landmarks, width, height)
            draw_indexfinger(img, hand_landmarks, width, height)
            draw_middlefinger(img, hand_landmarks, width, height)
            draw_ringfinger(img, hand_landmarks, width, height)
            draw_pinky(img, hand_landmarks, width, height)

            """ Gesture Recognition"""

            # all recognizable gestures
            pointer_up()
            thumbs_up()
            thumbs_down()
            finger_higher()
            fingers_two()
            fingers_three()
            fingers_five()
            fingers_four()

    cv2.imshow('Raw Webcam Feed', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
