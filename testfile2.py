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
import numpy as np

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
    image_array = numpy.array(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), dtype=np.uint16)
    if isinstance(imagematrix, str):
        imagematrix = image_array
    else:
        imagematrix = imagematrix + image_array
averageface = imagematrix / len(os.listdir(r"C:\Users\bram\testfolder"))
averageface = averageface.astype(numpy.uint8)


while True:
    cv2.imshow("Face", averageface)
    cv2.waitKey(1)