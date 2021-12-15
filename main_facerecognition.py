from typing import Any
import cv2
import os
import numpy as np
from numpy import linalg
from tqdm import tqdm
import mediapipe as mp
from math import sqrt
from time import sleep


# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


def lookingdirection(frame):
    mp_facemesh = mp.solutions.face_mesh
    face_mesh = mp_facemesh.FaceMesh()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if result.multi_face_landmarks is not None:
        for face_landmarks in result.multi_face_landmarks:
            for point in range(468):
                height, width, _ = frame.shape

                pointcoords = face_landmarks.landmark[point]
                x = int(pointcoords.x * width)  # x en y zijn genormaliseerd dus geeft het percentage aan
                # (als de foto 60 pixels breed is en x = 0.20, spreekt hij over xpixel 12)
                y = int(pointcoords.y * height)
            if face_landmarks.landmark[454].x - face_landmarks.landmark[1].x < 1 / 3 * (
                    face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                return "Right", img
            elif face_landmarks.landmark[454].x - face_landmarks.landmark[1].x > 2 / 3 * (
                    face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                return "Left", img
            else:
                return "Centered", img
    return None, img


def imagesizeconverter(x, y, w, h, gray, width, height):
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
    return img


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
    normalisedeigenvectors = normalisedeigenvectors
    transeigenv = normalisedeigenvectors.transpose()
    weights = np.dot(transeigenv, deviation_matrix.transpose())
    return weights


def normalise_lightlevel(imagematrix):
    median = np.median(imagematrix)
    differencefromnormal = 125 - median
    normalisedimage = imagematrix + differencefromnormal
    return normalisedimage


def eigenfacereconstruction(weights, normalisedeigenvectors, average):
    averagematrix = np.tile(average, (len(weights[0]), 1))
    deviation_per_image = np.dot(normalisedeigenvectors, weights).transpose()
    reconstructedimages = averagematrix + deviation_per_image
    return reconstructedimages


def readcam():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, img = cam.read();  # Makes a giant array of pixels
    return img


def facedetection(grayimage):
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    return faceDetect.detectMultiScale(grayimage, scaleFactor=1.2, minNeighbors=5)


def arraytoimage(array, width, height):
    image = np.reshape(array, (height, width))
    image = image.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image


def euclidiandistance(weights_eigenvectors, weights_detectedface):
    eucliddist = []
    for i in range(len(weights_eigenvectors)):
        eucliddist.append(np.linalg.norm(weights_detectedface - weights_eigenvectors[i, :]))
    return eucliddist


def eigenvectorselection(eigenvalues, eigenvectors):
    accuracy = 0
    numberofvectors = 0
    while accuracy < 0.99:
        numberofvectors += 1
        accuracy = np.sum(eigenvalues[:numberofvectors])/np.sum(eigenvalues)
    reducedeigenvectors = eigenvectors[:, :numberofvectors]
    return reducedeigenvectors


def threshold_for_euclidiandistance(weights_eigenvectors):
    rowdividedweights = weights_eigenvectors.transpose()
    maxeucdis = 0
    a = 0.7
    for i in rowdividedweights:
        for j in rowdividedweights:
            eucdis = np.linalg.norm(i-j)
            if eucdis > maxeucdis:
                maxeucdis = eucdis
    return a*maxeucdis


def facerecognition(image, x, y, w, h, directory, detectedface, averagefaceperplayer, eigenvectorsperplayer, weightsperplayer, thresholdperplayer, direction):
    matchpercentages = {}
    mineucliddistances = {}
    for i in os.listdir(directory):
        # Define where the library the recogniser has to use is located
        new_directory = 'looking' + str(direction)

        # Calculate the deviation for the detected face:
        deviation_detectedface = deviationmatrix([detectedface], averagefaceperplayer[i][new_directory])

        # Calculate the weights of the detected face
        weightvector_detectedface = weight(eigenvectorsperplayer[i][new_directory], deviation_detectedface)
        assert isinstance(weightvector_detectedface, np.ndarray)

        # Calculate Euclidian distance
        euclidian_distance = euclidiandistance(weightsperplayer[i][new_directory].transpose(), weightvector_detectedface.transpose())

        # Calculate if every Euclidian distance is below the threshold -> if so, face is a match!
        matchpercentages[i], mineucliddistances[i] = match(euclidian_distance, thresholdperplayer[i][new_directory])

    dataperplayer = {}

    # Already make a rectangle saying they are not recognized,
    # if they are recognized later this will be replaced by a red one
    cv2.rectangle(image, (x, y), (x + w, y + h),
                  (0, 255, 0), 2)

    # Combine all calculated data for this face into one dictionary for each player
    for i in matchpercentages:
        a = 1
        if matchpercentages[i] > 0.7:
            dataperplayer[i] = (a*mineucliddistances[i]/(matchpercentages[i]+1), matchpercentages[i], mineucliddistances[i])
    return image, dataperplayer


def match(eucdis, thresh):
    numberofmatches = 0
    mineucldist = 1000000
    for i in eucdis:
        if i < thresh:
            numberofmatches += 1
        if i < mineucldist:
            mineucldist = i
    matchpercentage = numberofmatches/len(eucdis)
    return matchpercentage, mineucldist


def minimumeuclidiandistance(dataperplayer):
    minimum = None
    for i in dataperplayer:
        for j in dataperplayer[i]:
            if minimum is None or dataperplayer[i][j][0] < minimum[2]:
                minimum = [i, j, dataperplayer[i][j][0], dataperplayer[i][j][1]]
    return minimum


def facialrecognition(image, eigenvectorsperplayer, averagefaceperplayer, thresholdperplayer, weightsperplayer, width,
                          height, directory):

        # First take a picture with the camera (we are going to be processing every frame it films)
        grayscale_picture = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect the position of all faces
        faces = facedetection(grayscale_picture)

        # Set up the dataperplayer dictionary and already integrate a section for each registered player
        listofdetectedplayers = os.listdir(directory)
        dataperplayer = {}
        for i in listofdetectedplayers:
            dataperplayer[i] = {}

        # Now try to recognize every face in the frame
        for (x, y, w, h) in faces:

            # Cut out the face from the image:
            reshapedface = imagesizeconverter(x, y, w, h, grayscale_picture, width, height)
            reshapedface = normalise_lightlevel(reshapedface)
            detectedface = imagetoarray(reshapedface)
            direction, image = lookingdirection(image)

            if direction is not None:

                # Perform the recognitionprogram on the face, returning a processed image and all data on the relations
                # between the playerlibraries and the face
                image, dataperplayerforface = facerecognition(image, x, y, w, h, directory, detectedface,
                                                              averagefaceperplayer, eigenvectorsperplayer,
                                                              weightsperplayer,
                                                              thresholdperplayer, direction)

                # Add the data for this face to the total pile of data
                for i in dataperplayerforface:
                    dataperplayer[i][(x, y, w, h)] = dataperplayerforface[i]

        resultingmatches = []
        while len(dataperplayer) > 0:
            # Calculate which face has the closest ressemblance to a player, and identify that one first
            result = minimumeuclidiandistance(dataperplayer)

            # If no faces were detected
            if result is None:
                dataperplayer = {}

            # Else at least one face was detected and has a matchpercentage of over 80 percent with one of the libraries
            else:
                player = result[0]
                coords = result[1]
                matchpercentage = result[3]

                resultingmatches.append((coords, player, matchpercentage))
                # Remove all appearances of those coords and player from the list, since these were matched together
                dataperplayer.pop(player)
                for i in dataperplayer:
                    if len(dataperplayer[i]) != 0 and coords in dataperplayer[i]:
                        dataperplayer[i].pop(coords)

                # Replace the "No Match" rectangle with the recognition rectangle
                (x, y, w, h) = coords
                cv2.rectangle(image, (x, y), (x + w, y + h),
                              (0, 0, 255), 2)
                cv2.putText(img=image, text=str(player), org=(x + w - 55, y + h + 20),
                            fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(0, 0, 255), thickness=1)
                cv2.putText(img=image, text=str(matchpercentage), org=(x + w - 55, y - 20),
                            fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(0, 0, 255), thickness=1)

        # Show the resulting processed image, indicating whether each face is recognized and who it would respond to
        return image, resultingmatches


def libraryprocessing(directory):

    """Database Processing"""
    eigenvectorsperplayer = {}
    averagefaceperplayer = {}
    thresholdperplayer = {}
    weightsperplayer = {}

    for i in os.listdir(directory):
        averagefaceperplayer[i] = {}
        eigenvectorsperplayer[i] = {}
        weightsperplayer[i] = {}
        thresholdperplayer[i] = {}

        for j in os.listdir(directory + str(r"\\") + str(i)):
            new_directory = directory + str(r"\\") + str(i) + str(r"\\") + str(j)

            # Convert the library of images into vectors and put them in a matrix
            librarymatrix = imagelibrarytomatrix(new_directory)

            # Calculate the average of the vectors in that matrix
            averagefaceperplayer[i][j] = meanofvectors(librarymatrix)

            # Calculate the deviation of the average for every image and put it into a matrix
            deviation_matrix = deviationmatrix(librarymatrix, averagefaceperplayer[i][j])

            # Calculate the Eigenvectors of the Covariancematrix
            eigenvalues, eigenvectors = eigcov(deviation_matrix)  # P is already normalized and is of form [U1 U2 U3 ...]
            # (so the vectors stored are the ROWS not the columns

            neweigenvectors = eigenvectorselection(eigenvalues, eigenvectors)

            # Store the eigenvectors of this player
            eigenvectorsperplayer[i][j] = neweigenvectors

            # Calculate the weight of each eigenvector
            weightsperplayer[i][j] = weight(neweigenvectors, deviation_matrix)

            # Use the weights to reconstruct the images,
            # if done correct you should have the exact same images that you started with
            # eigenfaces = eigenfacereconstruction(eigenvectorweights, eigenvectors, averageface)

            # OPTIONAL shows the first eigenface
            # image = arraytoimage(eigenfaces[0], width = 30, height = 40)
            # cv2.imshow("Eigenface1", image)
            # cv2.waitKey(10000)

            # Define the threshold for face detection
            thresholdperplayer[i][j] = threshold_for_euclidiandistance(weightsperplayer[i][j])
    return averagefaceperplayer, eigenvectorsperplayer, thresholdperplayer, weightsperplayer


class face_recognition:
    def __init__(self, directory):
        self.directory = directory
        averagefaceperplayer, eigenvectorsperplayer, thresholdperplayer, weightsperplayer = libraryprocessing(
            self.directory)
        assert isinstance(averagefaceperplayer, dict)
        self.averagefaceperplayer = averagefaceperplayer
        assert isinstance(eigenvectorsperplayer, dict)
        self.eigenvectorsperplayer = eigenvectorsperplayer
        assert isinstance(thresholdperplayer, dict)
        self.thresholdperplayer = thresholdperplayer
        assert isinstance(weightsperplayer, dict)
        self.weightsperplayer = weightsperplayer

    def faceRecognition(self, image, width = 30, height = 40):
        editedimage, resulting_matches = facialrecognition(image, self.eigenvectorsperplayer, self.averagefaceperplayer,
                                                          self.thresholdperplayer, self.weightsperplayer, width, height,
                                                          self.directory)
        return editedimage, resulting_matches


# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# instance = face_recognition(r'C:\Users\bram\testfolder')
# while True:
#     ret, img = cam.read()
#     image, resultingmatches = instance.faceRecognition(img)
#     cv2.imshow("Face", image)
#     cv2.waitKey(1)
#     print(resultingmatches)




