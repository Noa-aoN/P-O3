# Pip install Jupyter
# Pip install facenet-pytorch
# Type jupyter notebook in terminal

from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from typing import Any
import cv2
import os
import numpy as np
from numpy import linalg
from tqdm import tqdm
import mediapipe as mp
from math import sqrt
from time import sleep


def cropped_faces_from_image(image):
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_classifier.detectMultiScale(image, 1.3, 5)
    facelist = []
    for (x, y, w, h) in faces:
        facelist.append((image[y:y + h, x:x + w], (x, y, w, h)))
    return facelist


def draw_rectangle(image, coords, colour=(0,255,0)):
    assert isinstance(coords, tuple)
    assert isinstance(colour, tuple)
    (x, y, w, h) = coords
    cv2.rectangle(image, (x, y), (x + w, y + h),
                  colour, 2)
    cv2.waitKey(1)
    return image


def facenet_setup():
    imagesize = 160
    margin = 0.2
    # If required, create a face detection pipeline using MTCNN:
    mtcnn = MTCNN(image_size=imagesize, margin=margin)
    # Create an inception resnet (in eval mode):
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    return mtcnn, resnet


def get_embedding(imagepath, mtcnn, resnet):
    if isinstance(imagepath, str):
        img = Image.open(imagepath)
    else:
        img = imagepath
    try:
        img_cropped = mtcnn(img)
        img_embedding = resnet(img_cropped.unsqueeze(0))
    except:
        img_embedding = None
    return img_embedding


def embedding_matching(embedding1, embedding2):
    return embedding1 @ embedding2.T


def image_matching(image1, image2, mctnn=None, resnet=None):
    if mctnn is None or resnet is None:
        mctnn, resnet = facenet_setup()
    image1_embedding = get_embedding(image1, mctnn, resnet)
    image2_embedding = get_embedding(image2, mctnn, resnet)
    if image1_embedding is not None and image2_embedding is not None:
        result = embedding_matching(image1_embedding, image2_embedding)
    else:
         return 0
    return result[0]


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
        return None
    return directory


def comparison_with_library(image, librarydirectory):
    matchsum = 0
    matchaverage = 0
    highestmatchpercentage = 0
    mctnn, resnet = facenet_setup()
    for i in os.listdir(librarydirectory):
        libimg = Image.open(os.path.join(librarydirectory, i))
        matchpercent = image_matching(image, libimg, mctnn, resnet)
        if not isinstance(matchpercent, int):
            matchpercent = matchpercent.item()
        matchsum += matchpercent
        if matchpercent > highestmatchpercentage:
            highestmatchpercentage = matchpercent
    if len(os.listdir(librarydirectory)) != 0:
        matchaverage = matchsum/len(os.listdir(librarydirectory))
    return [matchaverage, highestmatchpercentage]


def library_imprint(directory, imagesperlibrary):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    numberofimages = 0
    while numberofimages < imagesperlibrary:
        ret, img = cam.read()
        faces = cropped_faces_from_image(img)
        if len(faces) == 1 and comparison_with_library(faces[0][0], directory)[0] < 0.85:
            numberofimages += 1
            cv2.imwrite(str(directory) + str(r"\image")+str(numberofimages)+str(".jpg"), faces[0][0])
        if len(faces) > 0:
            for i in range(len(faces)):
                img = draw_rectangle(img, faces[i][1])
        cv2.imshow("Face", img)
        cv2.waitKey(1)


def create_player_library(player, directory, imagesperlibrary):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if isinstance(player, str):
        new_directory = create_folder(directory + str(r"\\") + str(player))
    else:
        new_directory = create_folder(directory + str(r"\player") + str(player))
    if new_directory is None:
        return
    while True:
        ret, img = cam.read()
        cv2.putText(img=img, text=str("Press Enter to start taking pictures"), org=(0, 20), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5,
                    color=(0, 0, 255), thickness=1)
        cv2.putText(img=img, text=str("Hold Esc to stop PlayerRegistration"), org=(0, 40),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5,
                    color=(0, 0, 255), thickness=1)
        cv2.imshow("Face", img)
        if cv2.waitKey(1) & 0xff == 13:  # If you press Enter
            library_imprint(new_directory, imagesperlibrary)
            break
        elif cv2.waitKey(1) & 0xff == 27:  # If you press Escape
            print("Disengaging library_create for player" + str(player))
            break


def face_recognition(image, directory):
    faces = cropped_faces_from_image(image)
    identifiedfaces = set()
    resultlist = []
    for face in faces:
        image = draw_rectangle(image, face[1], (0, 255, 0))
        mostrepresentative = (face[1], None, 0, 0)
        for i in os.listdir(directory):
            [matchaverage, highestmatchpercentage] = \
                comparison_with_library(face[0], os.path.join(directory, i))
            if highestmatchpercentage > mostrepresentative[2] and matchaverage > 0.6 and highestmatchpercentage > 0.75\
                    and i not in identifiedfaces:
                mostrepresentative = (face[1], i, matchaverage, highestmatchpercentage)
                identifiedfaces.add(i)
                image = draw_rectangle(image, face[1], (0, 0, 255))
            elif highestmatchpercentage > mostrepresentative[2]:
                mostrepresentative = (face[1], None, matchaverage, highestmatchpercentage)
        resultlist.append(mostrepresentative)
    return image, resultlist


class PlayerRegistration:
    def __init__(self, librarydirectory, imagesperlibrary=10, playernr=1):
        assert isinstance(librarydirectory, str)
        self._directory = librarydirectory
        assert isinstance(playernr, int)
        self._playernr = playernr
        assert isinstance(imagesperlibrary, int)
        self._imagesperlibrary = imagesperlibrary

    def registerplayer(self, player=None):
        assert player is None or isinstance(player, str) or isinstance(player, int)
        if player is None:
            player = self._playernr
        create_player_library(player, self._directory, self._imagesperlibrary)
        if player not in os.listdir(self._directory):
            self._playernr += 1

    def identifyface(self, image):
        image, matches = face_recognition(image, self._directory)
        return image, matches


# Bram1 = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Bram1.jpg")
# Bram2 = Image.open(r'C:\Users\bram\facenetLibraries\Bram\image4.jpg')
# Karel = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Karel.jpg")
# print(embedding_matching(Bram1, Gorjan1))


# library = PlayerRegistration(r'C:\Users\bram\facenetLibraries', 10)
# library.registerplayer("Bram")

# print(image_matching(Bram2, Bram2))
# print(comparison_with_library(Karel, r'C:\Users\bram\facenetLibraries\Bram'))


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
instance = PlayerRegistration(r'C:\Users\bram\facenetLibraries')
while True:
    ret, img = cam.read()
    img, resultingmatches = instance.identifyface(img)
    cv2.imshow("Face", img)
    cv2.waitKey(1)
    print(resultingmatches)