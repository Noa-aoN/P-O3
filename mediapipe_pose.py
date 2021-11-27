import cv2
import mediapipe as mp
from math import sqrt

"""
later kunnen we dit gebruiken om de handen met de lichamen te verbinden om te zien van wie welk gebaar is
link: https://google.github.io/mediapipe/solutions/pose.html
"""


def linkfacewithhand(image, facecoords, wristcoords):
    try:
        assert isinstance(facecoords, tuple) and len(facecoords) == 4
        assert isinstance(wristcoords, tuple) and len(wristcoords) == 2
        height, width, _ = image.shape
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        with mp_pose.Pose(min_detection_confidence=0.5,  # standard
                          min_tracking_confidence=0.5) as pose:  # standard
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = pose.process(image)
            pose_landmarks = result.pose_landmarks
            if result.pose_landmarks is not None:
                (facex, facey, facew, faceh) = facecoords
                (handx, handy) = wristcoords
                mp_drawing.draw_landmarks(
                    image,
                    result.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                image = cv2.circle(image,
                                   (int(pose_landmarks.landmark[0].x * width), int(pose_landmarks.landmark[0].y * height)),
                                   2,
                                   (0, 255, 0), 2)
                if facex < pose_landmarks.landmark[7].x * width < facex + facew and \
                        facey < pose_landmarks.landmark[7].y * height < facey + faceh:
                    handpositions = [(pose_landmarks.landmark[15].x * width, pose_landmarks.landmark[15].y * height),
                                        (pose_landmarks.landmark[16].x * width, pose_landmarks.landmark[16].y * height)]
                    if sqrt((handx - handpositions[0][0]) ** 2 + (handy - handpositions[0][1]) ** 2) < 10 or \
                            sqrt((handx - handpositions[1][0]) ** 2 + (handy - handpositions[1][1]) ** 2) < 10:
                        return image, True
        return image, False
    except:
        return image, False


# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# facex = 500
# facey = 300
# facew = 300
# faceh = 300
# handx = 1000
# handy = 300
# while True:
#     ret, img = cam.read()
#     cv2.rectangle(img, (facex, facey), (facex + facew, facey + faceh),
#                   (0,0,0), 2)
#     cv2.rectangle(img, (handx-10, handy-10), (handx + 10, handy+10),
#                   (0, 0, 0), 2)
#     img, Bool = linkfacewithhand(img, (facex, facey, facew, faceh), (handx, handy))
#     if Bool:
#         print("match!")
#         break
#     cv2.imshow("Face", img)
#     cv2.waitKey(1)