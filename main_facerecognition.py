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

listofplayers = os.listdir(directory)


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
    transeigenv = normalisedeigenvectors.transpose()
    weights = np.dot(transeigenv, deviation_matrix.transpose())
    return weights


def normalise_lightlevel(imagematrix):
    minvalue = np.amin(imagematrix)
    normalisedimage = imagematrix - minvalue
    return normalisedimage


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
    a = 0.5
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
    if numberofmatches >= len(eucdis)/2:
        return True
    return False


def __main__():

    """Database Processing"""
    eigenvectorsperplayer = {}
    averagefaceperplayer = {}
    thresholdperplayer = {}

    for i in os.listdir(directory):
        new_directory = directory + str(r"\p") + str(i[1:])

        # Convert the library of images into vectors and put them in a matrix
        librarymatrix = imagelibrarytomatrix(new_directory)

        # Calculate the average of the vectors in that matrix
        averagefaceperplayer[i] = meanofvectors(librarymatrix)

        # Calculate the deviation of the average for every image and put it into a matrix
        deviation_matrix = deviationmatrix(librarymatrix, averagefaceperplayer[i])

        # Calculate the Eigenvectors of the Covariancematrix
        eigenvalues, eigenvectors = eigcov(deviation_matrix)  # P is already normalized and is of form [U1 U2 U3 ...]
        # (so the vectors stored are the ROWS not the columns

        # Store the eigenvectors of this player
        eigenvectorsperplayer[i] = eigenvectors

        # Calculate the weight of each eigenvector
        eigenvectorweights = weight(eigenvectors, deviation_matrix)

        # Use the weights to reconstruct the images,
        # if done correct you should have the exact same images that you started with
        # eigenfaces = eigenfacereconstruction(eigenvectorweights, eigenvectors, averageface)

        # OPTIONAL shows the first eigenface
        # image = arraytoimage(eigenfaces[0])
        # cv2.imshow("Eigenface1", image)
        # cv2.waitKey(10000)

        # Define the threshold for face detection
        thresholdperplayer[i] = threshold_for_euclidiandistance(eigenvectorweights)

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
            reshapedface = imagesizeconverter(x, y, w, h, grayscale_picture)
            reshapedface = normalise_lightlevel(reshapedface)
            detectedface = imagetoarray(reshapedface)
            for i in os.listdir(directory):

                # Calculate the deviation for the detected face:
                deviation_detectedface = deviationmatrix([detectedface], averagefaceperplayer[i])

                # Calculate the weights of the detected face
                weightvector_detectedface = weight(eigenvectorsperplayer[i], deviation_detectedface)
                assert isinstance(weightvector_detectedface, np.ndarray)

                # Calculate Euclidian distance
                euclidian_distance = euclidiandistance(eigenvectorweights.transpose(), weightvector_detectedface.transpose())

                # Calculate if every Euclidian distance is below the threshold -> if so, face is a match!
                matchfound = False
                if match(euclidian_distance, thresholdperplayer[i]):
                    cv2.rectangle(image, (x, y), (x+w, y+h),
                                  (0, 0, 255), 2)
                    cv2.putText(
                        img=image,
                        text=str(i),
                        org=(x+w-55, y+h+20),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=0.5,
                        color=(0, 0, 255),
                        thickness=1)
                    matchfound = True
                    break
            if not matchfound:
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



