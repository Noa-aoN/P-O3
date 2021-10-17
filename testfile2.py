import cv2
import mediapipe as mp


cap = cv2.VideoCapture(0)
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_facemesh = mp.solutions.face_mesh
face_mesh = mp_facemesh.FaceMesh()
# mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1)

with mp_holistic.Holistic(min_detection_confidence = 0.7, min_tracking_confidence = 0.7) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = holistic.process(img)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # print(results.face_landmarks)

        # for i in mp_holistic.FACEMESH_TESSELATION:
        #     print(i)


        mp_drawing.draw_landmarks(img, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                  mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 1, circle_radius = 1),
                                  mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1))
        #
        # mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
        #                           mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 1, circle_radius = 1),
        #                           mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1))
        #
        # mp_drawing.draw_landmarks(img, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        #                           mp_drawing.DrawingSpec(color = (0, 0, 255), thickness = 2, circle_radius =3),
        #                           mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1))

        cv2.imshow('Raw Webcam Feed', img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
