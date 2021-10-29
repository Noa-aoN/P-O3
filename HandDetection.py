import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    croppedconvertedimg = cv2.cvtColor(img[100:300, 100:300], cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, convertedimg) = cv2.threshold(croppedconvertedimg, 127, 255, cv2.THRESH_BINARY)
    img[100:300, 100:300] = convertedimg
    cv2.imshow("test", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()