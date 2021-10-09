import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([160,40,150])
    upper_red = np.array([180,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask=mask)


    frame_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(frame_gray, 10, 0.9, 7)
    if not corners is None:
        corners = np.int0(corners)

        for corner in corners:
            x,y = corner.ravel()
            cv2.circle(frame, (x,y), 5, (0,0,255), -1)

    cv2.imshow('frame', frame)
    cv2.imshow('hsv', result)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
