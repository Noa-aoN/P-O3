import cv2
import os
import numpy as np
from numpy import linalg
from tqdm import tqdm

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0)
directory = r'C:\Users\bram\testfolder'


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


def imagetoarray(imagematrix):
    return imagematrix.flatten()


def imagelibrarytomatrix(dir):
    dirlist_of_images = os.listdir(dir)
    imagearray_list = []
    print("Converting Library to matrix")
    for i in tqdm(dirlist_of_images):
        image = cv2.imread(os.path.join(dir, i))
        grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imagevector = imagetoarray(grayimage)
        imagearray_list.append(imagevector)
    librarymatrix = np.vstack(imagearray_list)
    return librarymatrix


def meanofvectors(numpy_matrix):
    return np.mean(numpy_matrix, axis=0)


def deviationmatrix(imagearraylist, average):
    deviationarray_list = []
    for i in tqdm(range(len(imagearraylist))):
        deviationvector = imagearraylist[i] - average
        deviationarray_list.append(deviationvector)
    deviation_matrix = np.vstack(deviationarray_list)
    return deviation_matrix


def eigcov(devmatrix):
    cov = (1/len(devmatrix)) * np.dot(devmatrix.transpose(), devmatrix)
    eigenValues, eigenVectors = np.linalg.eig(cov)
    idx = eigenValues.argsort()[::-1]
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:, idx]
    return eigenValues, eigenVectors


def reducedeigcov(devmatrix):
    reducedcov = dot(devmatrix, devmatrix.transpose())
    D, P = np.linalg.eig(reducedcov)
    return


def normofmatrixvectors(matrix):
    normalisedmatrix = []
    for i in tqdm(range(len(matrix))):
        vector = matrix[i]
        norm = np.linalg.norm(vector)
        normalisedmatrix.append(vector/norm)
    normalisedmatrix = np.vstack(normalisedmatrix)
    return normalisedmatrix


def weight(normalisedeigenvectors, deviation_matrix):
    transeigenv = normalisedeigenvectors.transpose()
    weights = np.dot(transeigenv, deviation_matrix.transpose())
    return weights


def eigenfacereconstruction(weights, normalisedeigenvectors, average):
    averagematrix = np.tile(average, (len(normalisedeigenvectors[0]), 1))
    deviationperimage = np.dot(normalisedeigenvectors, weights).transpose()
    reconstructedimages = averagematrix + deviationperimage
    return reconstructedimages


def __main__():

    # Convert the library of images into vectors and put them in a matrix
    librarymatrix = imagelibrarytomatrix(directory)

    # Calculate the average of the vectors in that matrix
    averageface = meanofvectors(librarymatrix)

    # Calculate the deviation of the average for every image and put it into a matrix
    deviation_matrix = deviationmatrix(librarymatrix, averageface)

    # Calculate the Eigenvectors of the Covariancematrix
    eigenvalues, eigenvectors = eigcov(devmatrix)  # P is already normalized and is of form [U1 U2 U3 ...]
    # (so the vectors stored are the ROWS not the columns

    # Calculate the weight of each eigenvector
    weights = weight(P, deviation_matrix)

    # Use the weights to reconstruct the images,
    # if done correct you should have the exact same images that you started with
    eigenfaces = eigenfacereconstruction(weights, eigenvectors, averageface)




def __alt__():

    librarymatrix = [[1, -2, 1, -3],
                     [1, 3, -1, 2],
                     [2, 1, -2, 3],
                     [1, 2, 2, 1]]
    average = meanofvectors(librarymatrix)
    deviation_matrix = deviationmatrix(librarymatrix, average)
    D, P = eigcov(deviation_matrix)
    weights = weight(P,deviation_matrix)
    eigenfaces = eigenfacereconstruction(weights, P, average)
    print(eigenfaces)





__main__()
# __alt__()



