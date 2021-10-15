import cv2
import os
import numpy as np
from numpy import linalg
from tqdm import tqdm

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0)
directory = r'C:\Users\bram\testfolder'
width = 60
height = 80


def imagesizeconverter(x, y, w, h):
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
    for i in range(len(imagearraylist)):
        deviationvector = imagearraylist[i] - average
        deviationarray_list.append(deviationvector)
    deviation_matrix = np.vstack(deviationarray_list)
    return deviation_matrix


def eigcov(devmatrix):
    cov = (1/len(devmatrix)) * np.dot(devmatrix.transpose(), devmatrix)
    print("Calculating Eigenvalues...")
    eigenValues, eigenVectors = np.linalg.eig(cov)
    eigenVectors = eigenVectors.real
    print("Done!")
    idx = eigenValues.argsort()[::-1]
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:, idx]
    return eigenValues, eigenVectors


def reducedeigcov(devmatrix):
    reducedcov = dot(devmatrix, devmatrix.transpose())
    D, P = np.linalg.eigh(reducedcov)
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
    averagematrix = np.tile(average, (len(weights[0]), 1))
    deviation_per_image = np.dot(normalisedeigenvectors, weights).transpose()
    reconstructedimages = averagematrix + deviation_per_image
    return reconstructedimages


def readcam():
    ret, img = cam.read();  # Makes a giant array of pixels
    return img


def facedetection(grayimage):
    return faceDetect.detectMultiScale(grayimage, scaleFactor=1.2, minNeighbors=5)


def arraytoimage(array):
    image = np.reshape(array, (height, width))
    image = image.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


def euclidiandistance(weights_eigenvectors, weights_detectedface):
    eucliddist = []
    for i in range(len(weights_eigenvectors)):
        eucliddist.append(np.linalg.norm(weights_detectedface - weights_eigenvectors[i, :]))
    return eucliddist


def threshold_for_euclidiandistance(weights_eigenvectors):
    rowdividedweights = weights_eigenvectors.transpose()
    maxeucdis = 0
    a = 1
    for i in rowdividedweights:
        for j in rowdividedweights:
            eucdis = np.linalg.norm(i-j)
            if eucdis > maxeucdis:
                maxeucdis = eucdis
    return a*maxeucdis


def match(eucdis, thresh):
    numberofmatches = 0
    for i in eucdis:
        if i < thresh:
            numberofmatches += 1
    if numberofmatches == len(eucdis):
        return True
    return False


def __main__():

    """Database Processing"""

    # Convert the library of images into vectors and put them in a matrix
    librarymatrix = imagelibrarytomatrix(directory)

    # Calculate the average of the vectors in that matrix
    averageface = meanofvectors(librarymatrix)

    # Calculate the deviation of the average for every image and put it into a matrix
    deviation_matrix = deviationmatrix(librarymatrix, averageface)

    # Calculate the Eigenvectors of the Covariancematrix
    eigenvalues, eigenvectors = eigcov(deviation_matrix)  # P is already normalized and is of form [U1 U2 U3 ...]
    # (so the vectors stored are the ROWS not the columns

    # Calculate the weight of each eigenvector
    eigenvectorweights = weight(eigenvectors, deviation_matrix)

    # Use the weights to reconstruct the images,
    # if done correct you should have the exact same images that you started with
    # eigenfaces = eigenfacereconstruction(eigenvectorweights, eigenvectors, averageface)

    # OPTIONAL shows the first eigenface
    # image = arraytoimage(eigenfaces[0])
    # cv2.imshow("Eigenface1", image)
    # cv2.waitKey(10000)

    threshold = threshold_for_euclidiandistance(eigenvectorweights)

    """Face Recognition based on Images from the Camera"""

    while True:
        # First take a picture with the camera (we are going to be processing every frame it films)
        image = readcam()
        grayscale_picture = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect the position of all faces
        faces = facedetection(grayscale_picture)

        # Now try to recognize every face in the frame
        for (x, y, w, h) in faces:
            # Cut out the face from the image:
            facecoords = imagesizeconverter(x, y, w, h)
            detectedface = imagetoarray(grayscale_picture[facecoords[1]:facecoords[3],
                                        facecoords[0]:facecoords[2]])

            # Calculate the deviation for the detected face:
            deviation_detectedface = deviationmatrix([detectedface], averageface)

            # Calculate the weights of the detected face
            weightvector_detectedface = weight(eigenvectors, deviation_detectedface)
            assert isinstance(weightvector_detectedface, np.ndarray)

            # Calculate Euclidian distance
            euclidian_distance = euclidiandistance(eigenvectorweights.transpose(), weightvector_detectedface.transpose())

            # Calculate if every Euclidian distance is below the threshold -> if so, face is a match!
            if match(euclidian_distance, threshold):
                cv2.rectangle(image, (x, y), (x+w, y+h),
                              (0, 0, 255), 2)
            else:
                cv2.rectangle(image, (x, y), (x+w, y+h),
                              (255, 0, 0), 2)
        cv2.imshow("Face", image)
        cv2.waitKey(1);


def __alt__():

    librarymatrix = [[1, -2, 1, -3],
                     [1, 3, -1, 2],
                     [2, 1, -2, 3],
                     [1, 2, 2, 1]]
    average = meanofvectors(librarymatrix)
    deviation_matrix = deviationmatrix(librarymatrix, average)
    D, P = eigcov(deviation_matrix)
    weights = weight(P, deviation_matrix)
    eigenfaces = eigenfacereconstruction(weights, P, average)
    print(eigenfaces)


__main__()
# __alt__()



