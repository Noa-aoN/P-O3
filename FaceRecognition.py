import cv2
import numpy as np
import os

directory = r'C:\Users\bram\testfolder'

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0)


os.chdir(directory)
face=0
sampleNum = 0
while(True):
    ret,img=cam.read();  # Makes a giant array of pixels
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # Changes the array into grayscale
    faces=faceDetect.detectMultiScale(gray,1.3,5);  # This detects faces in a matrix
    for(x,y,w,h) in faces:
        face += 1;  # This stores amount of samples

        cv2.imwrite(str(directory)+str("\seenface")+str(face)+".jpg", gray[y-20:y+h+20,x-20:x+w+20])  # This stores the file on your computer
        cv2.rectangle(img,(x-20,y-20),(x+w+20,y+h+20),(0,255,0),2)  # This creates the rectangle around your face
        cv2.waitKey(1);  # This is a delay
    cv2.imshow("Face",img);  # This shows the camera image
    cv2.waitKey(1);
    sampleNum += 1
    if(sampleNum>20):
        break;
cam.release()
cv2.destroyAllWindows()