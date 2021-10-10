from imutils import paths
import pickle
import cv2
import os
import numpy

directory = r'C:\Users\bram\testfolder\s'

imagematrix = ""
for i in os.listdir(r"C:\Users\bram\testfolder"):
    filenamewithouts = i[1:]
    image_vector = numpy.array(cv2.imread(directory + str(filenamewithouts))).reshape(-1)
    if isinstance(imagematrix, str):
        imagematrix = numpy.matrix(image_vector)
    else:
        imagematrix = numpy.append(imagematrix, [image_vector], axis=0)
averageface = numpy.sum(imagematrix, axis=0)/len(os.listdir(r"C:\Users\bram\testfolder"))

variancematrix = ""
for i in os.listdir(r"C:\Users\bram\testfolder"):
    filenamewithouts = i[1:]
    image_vector = numpy.array(cv2.imread(directory + str(filenamewithouts))).reshape(-1)
    if isinstance(variancematrix, str):
        variancematrix = numpy.matrix(image_vector-averageface[0])
    else:
        subtraction = image_vector-averageface[0]
        variancematrix = numpy.append(variancematrix, subtraction, axis=0)
covariancematrix = numpy.dot(variancematrix.transpose(), variancematrix)
print("hello1")
P, D, V = numpy.linalg.svd(covariancematrix)
D = numpy.diag(D)
Eigenfaces = numpy.dot(variancematrix, numpy.dot(V, numpy.power(D, (-1/2))))





