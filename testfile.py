import cv2
import mediapipe as mp


cap = cv2.VideoCapture(0)
mp_facemesh = mp.solutions.face_mesh
face_mesh = mp_facemesh.FaceMesh()
# mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1)

while cap.isOpened():
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(img)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if result.multi_face_landmarks is not None:
        for face_landmarks in result.multi_face_landmarks:
            for point in range(468):
                height, width, _ = frame.shape

                pointcoords = face_landmarks.landmark[point]
                x = int(pointcoords.x * width) # x en y zijn genormaliseerd dus geeft het percentage aan
                # (als de foto 60 pixels breed is en x = 0.20, spreekt hij over xpixel 12)
                y = int(pointcoords.y * height)

                if point != 1 and point != 234 and point != 454:  # Point 1 is tip of nose, point 234 is right cheekbone, 454 is left cheekbone
                    cv2.circle(img, (x, y), 1, (0, 0, 0))
                else:
                    cv2.circle(img, (x, y), 5, (0, 0, 255))
            if face_landmarks.landmark[454].x - face_landmarks.landmark[1].x < 1/4*(face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                cv2.putText(
                    img=img,
                    text=str("Looking Left"),
                    org=(0, 20),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.5,
                    color=(0, 0, 255),
                    thickness=1)
            elif face_landmarks.landmark[454].x - face_landmarks.landmark[1].x > 3/4*(face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                cv2.putText(
                    img=img,
                    text=str("Looking Right"),
                    org=(0, 20),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.5,
                    color=(0, 0, 255),
                    thickness=1)
            else:
                cv2.putText(
                    img=img,
                    text=str("Looking Centered"),
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
