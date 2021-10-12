import cv2

image= cv.VideoCapture(0)

th, dst = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY)

print(dst)
