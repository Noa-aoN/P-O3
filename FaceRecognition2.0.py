from imutils import paths
import pickle
import cv2
import os
import numpy
from math import *
from numpy import linalg
from scipy.sparse.linalg import norm
from scipy.linalg import sqrtm
from tqdm import tqdm

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0)
directory = r'C:\Users\bram\testfolder\s'


def imagesizeconverter(x, y, w, h):
    width = 60
    height = 80
    if w != width or h != height:
        # We are gonna be using x+a and w-a to keep the center of the face in the center,
        # so now we have to find a to convert
        a = (w - width) / 2
        b = (h - height) / 2

        x += a
        y += b
    return [int(x), int(y), int(x + width), int(y + height)]


imagematrix = ""
for i in os.listdir(r"C:\Users\bram\testfolder"):
    filenamewithouts = i[1:]
    image = cv2.imread(directory + str(filenamewithouts))
    image_vector = numpy.array(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)).reshape(-1)
    if isinstance(imagematrix, str):
        imagematrix = numpy.matrix(image_vector)
    else:
        imagematrix = numpy.append(imagematrix, [image_vector], axis=0)
averageface = numpy.sum(imagematrix, axis=0) / len(os.listdir(r"C:\Users\bram\testfolder"))
print(averageface)
cv2.imshow("Face", averageface)
# variancematrix = ""
# for i in tqdm(os.listdir(r"C:\Users\bram\testfolder")):
#     filenamewithouts = i[1:]
#     image = cv2.imread(directory + str(filenamewithouts))   # os.path.join(arg1, arg2)
#     image_vector = numpy.array(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)).reshape(-1)
#     if isinstance(variancematrix, str):
#         variancematrix = numpy.matrix(image_vector - averageface[0])
#     else:
#         subtraction = image_vector - averageface[0]
#         variancematrix = numpy.append(variancematrix, subtraction, axis=0)
# covariancematrix = numpy.dot(variancematrix.transpose(), variancematrix)
averagematrix = numpy.tile(averageface, (len(os.listdir(r"C:\Users\bram\testfolder")), 1))
differencefromaverage = imagematrix - averagematrix
covariancematrix = numpy.cov(differencefromaverage.transpose(), bias=1)
D, V = linalg.eig(covariancematrix)
Eigenfaces = V



# get paths of each file in folder named Images
# Images here contains my data(folders of various persons)
face = 0
while True:
    ret, img = cam.read();  # Makes a giant array of pixels
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Changes the array into grayscale
    faces = faceDetect.detectMultiScale(gray, 1.3, 5);  # This detects faces in a matrix
    for (x, y, w, h) in faces:
        cv2.waitKey(1);  # This is a delay
        convertedimage = imagesizeconverter(x, y, w, h)
        vectornewface = numpy.array(gray[convertedimage[1]:convertedimage[3],
                                    convertedimage[0]:convertedimage[2]]).reshape(-1)
        weightvectornewface = numpy.dot(vectornewface - averageface, Eigenfaces.transpose())
        predefined_treshhold = 500000000000;
        match = 0;
        for i in range(len(os.listdir(r"C:\Users\bram\testfolder"))):
            euclidian_distance = numpy.linalg.norm(weightvectornewface - (numpy.dot(Eigenfaces, differencefromaverage[i, :].transpose())));
            if euclidian_distance < predefined_treshhold:
                match += 1
            if match == len(os.listdir(r"C:\Users\bram\testfolder")):
                cv2.rectangle(img, (convertedimage[0], convertedimage[1]), (convertedimage[2], convertedimage[3]),
                              (0, 0, 255), 2)
                cv2.imshow("Face", img)
            else:
                cv2.rectangle(img, (convertedimage[0], convertedimage[1]), (convertedimage[2], convertedimage[3]),
                              (255, 0, 0), 2)
                cv2.imshow("Face", img)
    cv2.imshow("Face", img);  # This shows the camera image
    cv2.waitKey(1);
    face += 1
    if face == 1000:
        break
cam.release()
cv2.destroyAllWindows()