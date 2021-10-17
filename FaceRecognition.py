import cv2
import numpy as np
import os

directory = r'C:\Users\bram\testfolder'

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0)


def imagesizeconverter (x, y, w, h):
    width = 60
    height = 80
    if w != width or h != height:
        # We are gonna be using x+a and w-a to keep the center of the face in the center,
        # so now we have to find a to convert
        a = (w-width)/2
        b = (h-height)/2

        x += a
        y += b
    return [int(x), int(y), int(x+width), int(y+height)]


def normalise_lightlevel(imagematrix):
    minvalue = np.amin(imagematrix)
    normalisedimage = imagematrix - minvalue
    return normalisedimage


os.chdir(directory)
face=0
sampleNum = 0

while(True):
    ret,img=cam.read();  # Makes a giant array of pixels
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # Changes the array into grayscale
    faces=faceDetect.detectMultiScale(gray,1.3,5);  # This detects faces in a matrix
    for(x,y,w,h) in faces:
        face += 1;  # This stores amount of samples
        convertedimage = imagesizeconverter(x,y,w,h)
        normalisedimage = normalise_lightlevel(gray[convertedimage[1]:convertedimage[3],convertedimage[0]:convertedimage[2]])

        cv2.imwrite(str(directory)+str("\seenface")+str(face)+".jpg", normalisedimage)  # This stores the file on your computer
        cv2.rectangle(img, (convertedimage[0],convertedimage[1]),(convertedimage[2],convertedimage[3]),(0,255,0),2)  # This creates the rectangle around your face
        cv2.waitKey(1);  # This is a delay
    cv2.imshow("Face",img);  # This shows the camera image
    cv2.waitKey(1);
    sampleNum += 1
    if(sampleNum>20):
        break;
cam.release()
cv2.destroyAllWindows()
