import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([100,100,0])
    upper_red = np.array([180,255,255])

    lower_white = np.array([0,0,215])
    upper_white = np.array([40,35,255])

    lower_black = np.array([0,0,0])
    upper_black = np.array([50,5,5])

    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    result_white = cv2.bitwise_and(frame, frame, mask=mask_white)
    result_black = cv2.bitwise_and(frame,frame, mask=mask_black)

    frame_red_gray = cv2.cvtColor(result_red, cv2.COLOR_BGR2GRAY)
    frame_white_gray = cv2.cvtColor(result_white, cv2.COLOR_BGR2GRAY)
    frame_black_gray = cv2.cvtColor(result_black, cv2.COLOR_BGR2GRAY)

    corners_red = cv2.goodFeaturesToTrack(frame_red_gray, 10, 0.99, 7)
    corners_white = cv2.goodFeaturesToTrack(frame_white_gray, 10, 0.9, 7)
    corners_black = cv2.goodFeaturesToTrack(frame_black_gray, 10, 0.99, 7)

    if not corners_red is None:
        corners_red = np.int0(corners_red)

        for corner in corners_red:
            x,y = corner.ravel()
            cv2.circle(frame, (x,y), 5, (0,0,255), -1)

    if not corners_white is None:
        corners_white = np.int0(corners_white)

        for corner in corners_white:
            x,y = corner.ravel()
            #cv2.circle(frame, (x,y), 5, (255,255,255), -1)

    if not corners_black is None:
        corners_black = np.int0(corners_black)

        for corner in corners_black:
            x,y = corner.ravel()
            cv2.circle(frame, (x,y), 5, (40,110,70), -1)

    cv2.imshow('hsv_red', result_red)
    #cv2.imshow('hsv_white', result_white)
    cv2.imshow('hsv_black', result_black)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
