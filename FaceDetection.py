import cv2
import numpy as np
import os
import mediapipe as mp

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
width = 60
height = 80


def imagesizeconverter(x, y, w, h, gray):
    heighttowidthratio = width/height
    x += 0.2*w
    w -= 0.4*w
    y += 0.2*h
    h -= 0.2*h
    if w/h < heighttowidthratio:
        compensation = heighttowidthratio*h - w
        x -= compensation/2
        w += compensation
    else:
        compensation = w - heighttowidthratio*h
        x -= compensation/2
        w += compensation
    img = gray[int(y):int(y+h), int(x):int(x+w),]
    img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)
    cv2.imshow("Resized", img)
    return img, int(x), int(y), int(w), int(h)


while True:
    ret, img = cam.read();  # Makes a giant array of pixels
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        image, x, y, w, h = imagesizeconverter(x, y, w, h, gray)
        cv2.waitKey(1)
        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)
        cv2.imshow("Full Screen", img)
cam.release()
cv2.destroyAllWindows()