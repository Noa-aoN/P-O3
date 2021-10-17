import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
# mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1)

while cap.isOpened():
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(img)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if result.multi_hand_landmarks is not None:
        for hand_landmarks in result.multi_hand_landmarks:
            for point in range(21):
                width, height, _ = frame.shape

                pointcoords = hand_landmarks.landmark[point]
                x = int(pointcoords.x * width)  # x en y zijn genormaliseerd dus geeft het percentage aan
                # (als de foto 60 pixels breed is en x = 0.20, spreekt hij over xpixel 12)
                y = int(pointcoords.y * height)
                # cv2.line(img, (points[0]), (points[1]), (0, 255, 0), thickness=3, lineType=8)
                cv2.circle(img, (x, y), 2, (0, 0, 255))

            """Connecting the right dots to have a nicely looking hand"""

            # Thumb:
            cv2.line(img, (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
                     (int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height)),
                     (0, 255, 0), thickness=1)
            cv2.line(img, (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height)),
                     (int(hand_landmarks.landmark[3].x * width), int(hand_landmarks.landmark[3].y * height)),
                     (0, 255, 0), thickness=1)

            # IndexFinger:
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

            """ Gesture Recognition"""

            # Pointerfinger up ("higher")
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

            elif hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y < hand_landmarks.landmark[2].y < \
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

            elif hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y < hand_landmarks.landmark[6].y < \
                    hand_landmarks.landmark[5].y and \
                    hand_landmarks.landmark[12].y > hand_landmarks.landmark[11].y > hand_landmarks.landmark[10].y and \
                    hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y > hand_landmarks.landmark[14].y and \
                    hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y > hand_landmarks.landmark[18].y:
                cv2.putText(
                    img=img,
                    text=str("Higher"),
                    org=(0, 20),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.5,
                    color=(0, 0, 255),
                    thickness=1)

    cv2.imshow('Raw Webcam Feed', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
