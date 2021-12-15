import traceback
import cv2
import numpy as np
import math
import mediapipe as mp
import matplotlib.pyplot as plt

"""
link: https://stackoverflow.com/questions/57525324/how-to-detect-number-of-fingers-and-add-double-digits-using-opencv
uitleg convex hull: http://www.ripublication.com/ijaer17/ijaerv12n18_04.pdf 
                    https://brilliant.org/wiki/convex-hull/
"""

"""
OPENCV
"""


def gesture_recognition():
    cap = cv2.VideoCapture(0)  # 0 voor webcam, 1 voor USB-camera

    for u in range(50):

        try:  # an error comes if it does not find anything in window as it cannot find contour of max area
            # therefore this try error statement
            # error vermijden

            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            kernel = np.ones((3, 3), np.uint8)

            # region of interest, gebied dat de camera bekijkt
            roi = frame[100:300, 100:300]

            # rechthoek rond roi maken
            cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)  # hsv kleuren makkelijker te herkennen?

            # range voor huidskleuren definieren om achtergrond uit te filteren
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)

            # huidskleur uit beeld halen
            mask = cv2.inRange(hsv, lower_skin, upper_skin)

            # hand uit het beeld halen??
            mask = cv2.dilate(mask, kernel, iterations=4)

            # blur toevoegen
            mask = cv2.GaussianBlur(mask, (5, 5), 100)

            # contouren zoeken
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # print(contours)
            # print(hierarchy)
            # grootste contour vinden (hand)
            cnt = max(contours, key=lambda x: cv2.contourArea(x))

            # contour benaderen??
            epsilon = 0.0005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # convex hull rond hand maken, zie algoritme online
            hull = cv2.convexHull(cnt)

            # oppervlakte van hull en oppervlakte van hand/contour
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)

            # percentage van oppervlakte van convex hull zoeken die niet door hand bedekt is
            arearatio = ((areahull - areacnt) / areacnt) * 100

            # aantal defecten in hull zoeken = aantal vingers?
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)

            # l = no. of defects
            l = 0

            # aantal defecten vinden
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt = (100, 180)

                # lengtes van de zijden van driehoek berekenen
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                s = (a + b + c) / 2
                ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                # distance between point and convex hull
                d = (2 * ar) / a

                # cosinusregel
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                # hoeken groter dan 90 graden negeren en punten dichtbij hull ook negeren, zorgt voor betere nauwkeurigheid
                if angle <= 90 and d > 30:
                    l += 1
                    cv2.circle(roi, far, 3, [255, 0, 0], -1)

                # lijn rond hand tekenen
                cv2.line(roi, start, end, [0, 255, 0], 2)

            l += 1

            # juiste tekst weergeven
            font = cv2.FONT_HERSHEY_DUPLEX
            if l == 1:
                if areacnt < 2000:  # oppervlakte contour rond hand
                    cv2.putText(frame, 'Geen hand zichtbaar', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                else:
                    if arearatio < 12:
                        cv2.putText(frame, '0', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    elif arearatio < 17.5:
                        cv2.putText(frame, '?', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

                    else:
                        cv2.putText(frame, '1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            elif l == 2:
                cv2.putText(frame, '2', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            elif l == 3:

                if arearatio < 27:
                    cv2.putText(frame, '3', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                else:
                    # wat doet de volgende lijn?
                    cv2.putText(frame, 'ok', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            elif l == 4:
                cv2.putText(frame, '4', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            elif l == 5:
                cv2.putText(frame, '5', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            elif l == 6:
                cv2.putText(frame, 'reposition', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            else:
                cv2.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

            # windows laten zien
            cv2.imshow('mask', mask)  # laat zien wat de camera als hand waarneemt
            cv2.imshow('frame', frame)
        except Exception:
            traceback.print_exc()
            pass
        # break


    cv2.destroyAllWindows()
    cap.release()
    return l


def init_camera(source=1):
    cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    return cap


"""
MEDIAPIPE
"""



def index_up(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y > hand_landmarks.landmark[11].y > hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y > hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        return True
    return False


def fingers_two(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y > hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
        return True
    return False


def fingers_three(hand_landmarks):
    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
            hand_landmarks.landmark[5].y and \
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
            hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
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
        return True
    return False



def recognition():
    cap = init_camera(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # opencv gebruikt bgr!
    functions = {index_up: 1, fingers_four: 4, fingers_five: 5, fingers_three: 3, fingers_two: 2}
    if result.multi_hand_landmarks is not None:
        # all recognizable gestures, more can be implemented
        # allemaal if's toegevoegd zodat meerdere gebaren niet tegelijk kunnen herkend worden, simpelste gebaren vanboven

        for func in functions:
            if func(result.multi_hand_landmarks[0]):
                return functions[func]

    cap.release()


"""
TEST, x aantal testiteraties, test de nauwkeurigheid, niet de snelheid
"""


def test(x, fingers):
    count_cv = []
    count_mp = []
    for i in range(x):
        count_cv.append(gesture_recognition() == fingers)
        mp_gest = recognition()
        count_mp.append(mp_gest == fingers)
    result = {"cv": count_cv, "mp": count_mp}
    return result

iter = 15
gest = 3
test_gest = test(iter, gest) # eerste is aantal testen, tweede is aantal vingers
print(test_gest)
"""
bar plot voorbeeld

data = [23, 45, 56, 78, 213]
plt.bar([1,2,3,4,5], data)
plt.show()
"""
data = [test_gest["cv"].count(True) , test_gest["mp"].count(True), iter]
plt.bar(["cv", "mp", "total"], data)
plt.show()
