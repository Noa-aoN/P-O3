import cv2
import mediapipe as mp

"""
kan een heleboel gebaren herkennen via het vergelijken van de coordinaten van de 'landmarks'
er kunnen nog meer gebaren geimplementeerd worden
zelfde programma als 'gestures_mediapipe.py' maar dan in een klasse
link: 
https://optisol.com.au/insight/alphabet-hand-gestures-recognition-using-mediapipe/#:~:text=MediaPipe%20Hand%20is%20a%20machine%20learning%20employed%20high-fidelity,help%20of%20multiple%20models%20which%20are%20working%20simultaneously.
"""


class gesture_recognition:

    def index_down(self, img, hand_landmarks):
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
            print("lower")
            return True

    def thumbs_up(self, img, hand_landmarks):
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
            print("thumbs up")
            return True

    def thumbs_down(self, img, hand_landmarks):
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
            print("thumbs down")
            return True

    def index_up(self, img, hand_landmarks):
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
            print("higher/one")
            return True


    def fingers_two(self, img, hand_landmarks):
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
            print("two")
            return True


    def fingers_three(self, img, hand_landmarks):
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
            print("three")
            return True

    def fingers_five(self, img, hand_landmarks):
        if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
                hand_landmarks.landmark[5].y and \
                hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
                hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
                hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y and \
                abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[5].x) < \
                abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[
                    9].x):  # afstand van bovenkant duim tot onderkant van wijsvinger en middelvinger vergelijken
            cv2.putText(
                img=img,
                text=str("Five"),
                org=(0, 20),
                fontFace=cv2.FONT_HERSHEY_DUPLEX,
                fontScale=0.5,
                color=(0, 0, 255),
                thickness=1)
            print("five")
            return True

    def fingers_four(self, img, hand_landmarks):
        if hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
                hand_landmarks.landmark[5].y and \
                hand_landmarks.landmark[12].y < hand_landmarks.landmark[11].y < hand_landmarks.landmark[10].y and \
                hand_landmarks.landmark[16].y < hand_landmarks.landmark[15].y < hand_landmarks.landmark[14].y and \
                hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y < hand_landmarks.landmark[18].y and not \
                self.fingers_five(img, hand_landmarks):
            cv2.putText(
                img=img,
                text=str("Four"),
                org=(0, 20),
                fontFace=cv2.FONT_HERSHEY_DUPLEX,
                fontScale=0.5,
                color=(0, 0, 255),
                thickness=1)
            print("four")
            return True

    def draw_thumb(self, img, hand_landmarks, width, height):
        cv2.line(img, (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
                 (int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
                 (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
                 (0, 255, 0), thickness=1)

    def draw_index(self, img, hand_landmarks, width, height):
        cv2.line(img, (int(hand_landmarks.landmark[7].x * width), int(hand_landmarks.landmark[7].y * height)),
                 (int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height)),
                 (int(hand_landmarks.landmark[7].x * width), int(hand_landmarks.landmark[7].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height)),
                 (int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height)),
                 (0, 255, 0), thickness=1)

    def draw_middle(self, img, hand_landmarks, width, height):
        cv2.line(img, (int(hand_landmarks.landmark[11].x * width), int(hand_landmarks.landmark[11].y * height)),
                 (int(hand_landmarks.landmark[12].x * width), int(hand_landmarks.landmark[12].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height)),
                 (int(hand_landmarks.landmark[11].x * width), int(hand_landmarks.landmark[11].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[9].x * width), int(hand_landmarks.landmark[9].y * height)),
                 (int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height)),
                 (0, 255, 0), thickness=1)

    def draw_ring(self, img, hand_landmarks, width, height):
        cv2.line(img, (int(hand_landmarks.landmark[15].x * width), int(hand_landmarks.landmark[15].y * height)),
                 (int(hand_landmarks.landmark[16].x * width), int(hand_landmarks.landmark[16].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height)),
                 (int(hand_landmarks.landmark[15].x * width), int(hand_landmarks.landmark[15].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height)),
                 (int(hand_landmarks.landmark[13].x * width), int(hand_landmarks.landmark[13].y * height)),
                 (0, 255, 0), thickness=1)

    def draw_pinky(self, img, hand_landmarks, width, height):
        cv2.line(img, (int(hand_landmarks.landmark[19].x * width), int(hand_landmarks.landmark[19].y * height)),
                 (int(hand_landmarks.landmark[20].x * width), int(hand_landmarks.landmark[20].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height)),
                 (int(hand_landmarks.landmark[19].x * width), int(hand_landmarks.landmark[19].y * height)),
                 (0, 255, 0), thickness=1)
        cv2.line(img, (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height)),
                 (int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height)),
                 (0, 255, 0), thickness=1)

    def draw_palm(self, img, hand_landmarks, width, height):
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

    def draw_hand(self, img, hand_landmarks, width, height):
        self.draw_thumb(img, hand_landmarks, width, height)
        self.draw_index(img, hand_landmarks, width, height)
        self.draw_middle(img, hand_landmarks, width, height)
        self.draw_ring(img, hand_landmarks, width, height)
        self.draw_pinky(img, hand_landmarks, width, height)
        self.draw_palm(img, hand_landmarks, width, height)

    def recognition(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # , cv2.CAP_DSHOW
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()

        while cap.isOpened():  # main loop
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

                    self.draw_hand(img, hand_landmarks, width, height)

                    """ Gesture Recognition"""

                    # all recognizable gestures, more can be implemented
                    # allemaal if's toegevoegd zodat meerdere gebaren niet tegelijk kunnen herkend worden, simpelste gebaren vanboven
                    if self.index_down(img, hand_landmarks):
                        self.index_down(img, hand_landmarks)
                        return "index_down"
                    elif self.thumbs_up(img, hand_landmarks):
                        self.thumbs_up(img, hand_landmarks)
                        return "thumbs_up"
                    elif self.thumbs_down(img, hand_landmarks):
                        self.thumbs_down(img, hand_landmarks)
                        return "thumbs_down"
                    elif self.index_up(img, hand_landmarks):
                        self.index_up(img, hand_landmarks)
                        return "index_up"
                    elif self.fingers_five(img, hand_landmarks):
                        self.fingers_five(img, hand_landmarks)
                        return "five"
                    elif self.fingers_four(img, hand_landmarks):
                        self.fingers_four(img, hand_landmarks)
                        return "four"
                    elif self.fingers_three(img, hand_landmarks):
                        self.fingers_three(img, hand_landmarks)
                        return "three"
                    elif self.fingers_two(img, hand_landmarks):
                        self.fingers_two(img, hand_landmarks)
                        return "two"

            cv2.imshow('Raw Webcam Feed', img)

            if cv2.waitKey(10) & 0xFF == ord('q'):  # q om te stoppen
                break

        cap.release()
        cv2.destroyAllWindows()


# om programma te runnen:
# from gestures_mediapipe_class.py import gesture_recognition
# gesture_recognition().recognition()