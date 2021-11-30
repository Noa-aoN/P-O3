# Pip install Jupyter
# Pip install facenet-pytorch
# Type jupyter notebook in terminal

"""Both pretrained models were trained on 160x160 px images,
so will perform best if applied to images resized to this shape.
For best results, images should also be cropped to the face using MTCNN (see below)."""

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


def draw_rectangle(image, coords, colour=(0, 255, 0)):
    assert isinstance(coords, tuple)
    assert isinstance(colour, tuple)
    (x, y, w, h) = coords
    cv2.rectangle(image, (x, y), (x + w, y + h),
                  colour, 2)
    cv2.waitKey(1)
    return image


def facenet_setup(imagesize=160, margin=0.2):
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
    if embedding1 is None or embedding2 is None:
        return 0
    return embedding1 @ embedding2.T


def image_matching(image1, image2, mtcnn=None, resnet=None):
    if mtcnn is None or resnet is None:
        mtcnn, resnet = facenet_setup()
    image1_embedding = get_embedding(image1, mtcnn, resnet)
    image2_embedding = get_embedding(image2, mtcnn, resnet)
    if image1_embedding is not None and image2_embedding is not None:
        result = embedding_matching(image1_embedding, image2_embedding)
    else:
        return 0
    return result[0]


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        # elif len(os.listdir(directory)) > 0:
        #     return 'exists'
            # ans = input('A library with this directory already exists. Do you want to replace its contents? '
            #             '(type yes or 1 if you want to replace)')
            # if ans == 'yes' or ans == '1':
            #     clear_folder_contents(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
        return None
    return directory


def clear_folder_contents(directory):
    for i in os.listdir(directory):
        os.remove(os.path.join(directory, i))


def looking_direction(face):
    face = np.array(face)
    mp_facemesh = mp.solutions.face_mesh
    face_mesh = mp_facemesh.FaceMesh()
    img = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(img)
    xaxis = None
    yaxis = None
    if result.multi_face_landmarks is not None:
        for face_landmarks in result.multi_face_landmarks:

            # Face rotation around the y-axis
            if face_landmarks.landmark[454].x - face_landmarks.landmark[1].x < 1 / 3 * (
                    face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                yaxis = "Left"
            elif face_landmarks.landmark[454].x - face_landmarks.landmark[1].x > 2 / 3 * (
                    face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                yaxis = "Right"
            else:
                yaxis = "Straight"

            # Face rotation around the x-axis
            if (face_landmarks.landmark[454].y + face_landmarks.landmark[234].y) / 2 - face_landmarks.landmark[
                1].y > 0.05:
                xaxis = "Up"
            elif (face_landmarks.landmark[454].y + face_landmarks.landmark[234].y) / 2 - face_landmarks.landmark[
                1].y < -0.12:
                xaxis = "Down"
            else:
                xaxis = "Centered"

    return (xaxis, yaxis)


def comparison_with_library(image, libraryembeddings, mtcnn, resnet):
    matchsum = 0
    matchaverage = 0
    highestmatchpercentage = 0
    image_embedding = get_embedding(image, mtcnn, resnet)
    if image_embedding is not None:
        for refimg_embedding in libraryembeddings:
            matchpercent = embedding_matching(image_embedding, refimg_embedding)
            if not isinstance(matchpercent, int):
                matchpercent = matchpercent.item()
            matchsum += matchpercent
            if matchpercent > highestmatchpercentage:
                highestmatchpercentage = matchpercent
        if len(libraryembeddings) != 0:
            matchaverage = matchsum / len(libraryembeddings)
    return [matchaverage, highestmatchpercentage]


def library_imprint(directory, imagesperlibrary, mtcnn, resnet):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    numberofimages = 0
    if len(os.listdir(directory)) > 0:
        numberofimages += len(os.listdir(directory))
    embeddings = []
    directions = set()
    wanteddirections = {("Up", "Left"), ("Up", "Straight"), ("Up", "Right"),
                        ("Centered", "Left"), ("Centered", "Straight"), ("Centered", "Right"),
                        ("Down", "Left"), ("Down", "Straight"), ("Down", "Right")}
    while numberofimages < imagesperlibrary:
        ret, img = cam.read()
        faces = cropped_faces_from_image(img)
        if len(faces) == 1 and comparison_with_library(faces[0][0], embeddings, mtcnn, resnet)[0] < 0.85:
            face_embedding = get_embedding(faces[0][0], mtcnn, resnet)
            direction = looking_direction(faces[0][0])
            if face_embedding is not None:
                if len(directions) < 9 and direction[0] is not None and direction[1] is not None and \
                        direction not in directions:
                    wanteddirections.remove(direction)
                    embeddings.append(face_embedding)
                    directions.add(direction)
                    numberofimages += 1
                    cv2.imwrite(str(directory) + str(r"\image") + str(numberofimages) + str(".jpg"), faces[0][0])
                elif len(directions) >= 9:
                    embeddings.append(face_embedding)
                    numberofimages += 1
                    cv2.imwrite(str(directory) + str(r"\image") + str(numberofimages) + str(".jpg"), faces[0][0])
        if len(faces) > 0:
            for i in range(len(faces)):
                img = draw_rectangle(img, faces[i][1])
                cv2.putText(img=img, text=str(str(numberofimages) + str(
                    " have been taken. " + str(imagesperlibrary - numberofimages) + str(" more to go."))),
                            org=(0, 20), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(0, 0, 255),
                            thickness=1)
                pos = 1
                for (xaxis, yaxis) in wanteddirections:
                    cv2.putText(img=img, text=str(xaxis) + str(" ") + str(yaxis),
                                org=(1380, pos*20), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.6, color=(0, 0, 255),
                                thickness=1)
                    pos += 1
        cv2.imshow("Face", img)
        cv2.waitKey(1)
    return tuple(embeddings)


def create_player_library(player, directory, imagesperlibrary, mtcnn, resnet):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    new_directory = create_folder(os.path.join(directory, str(player)))
    if new_directory is None:
        return None
    while True:
        ret, img = cam.read()
        if cv2.waitKey(1) & 0xff == 13:  # If you press Enter
            embeddings = library_imprint(new_directory, imagesperlibrary, mtcnn, resnet)
            cv2.putText(img=img, text=str("Succesfully created library"), org=(0, 20),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5,
                        color=(0, 0, 255), thickness=1)
            cv2.imshow("Face", img)
            cv2.waitKey(1)
            cam.release()
            cv2.destroyAllWindows()
            return embeddings
        elif cv2.waitKey(1) & 0xff == 27:  # If you press Escape
            cv2.putText(img=img, text=str("Disengaging library_create for player" + str(player)), org=(0, 20),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5,
                        color=(0, 0, 255), thickness=1)
            cv2.imshow("Face", img)
            cv2.waitKey(1)
            cap.release()
            cv2.destroyAllWindows()
            return None
        cv2.putText(img=img, text=str("Press Enter to start taking pictures"), org=(0, 20),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5,
                    color=(0, 0, 255), thickness=1)
        cv2.putText(img=img, text=str("Hold Esc to stop PlayerRegistration"), org=(0, 40),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5,
                    color=(0, 0, 255), thickness=1)
        cv2.imshow("Face", img)


def library_embeddings(librarydirectory, mtcnn, resnet):
    embeddings = []
    for i in os.listdir(librarydirectory):
        face_embedding = get_embedding(os.path.join(librarydirectory, i), mtcnn, resnet)
        embeddings.append(face_embedding)
    return tuple(embeddings)


def face_recognition(image, mtcnn, resnet, libraryembeddings):
    faces = cropped_faces_from_image(image)
    identifiedfaces = set()
    resultlist = []
    for face in faces:
        image = draw_rectangle(image, face[1], (0, 255, 0))
        mostrepresentative = (face[1], None, 0, 0)
        for i in libraryembeddings:
            [matchaverage, highestmatchpercentage] = \
                comparison_with_library(face[0], libraryembeddings[i], mtcnn, resnet)
            if highestmatchpercentage > mostrepresentative[2] and matchaverage > 0.65 and highestmatchpercentage > 0.8 \
                    and i not in identifiedfaces:
                mostrepresentative = (face[1], i, matchaverage, highestmatchpercentage)
                identifiedfaces.add(i)
                image = draw_rectangle(image, face[1], (0, 0, 255))
            elif highestmatchpercentage > mostrepresentative[2]:
                mostrepresentative = (face[1], None, matchaverage, highestmatchpercentage)
        resultlist.append(mostrepresentative)
    return image, resultlist


def search_player(player, image, mtcnn, resnet, library):

    # Get the embeddings for only the registered faces of player in library
    if isinstance(library, str):
        if player not in os.listdir(library):
            print("Player not in Library")
            return []
        try:
            library_embedding = library_embeddings(os.path.join(library, player), mtcnn, resnet)
        except:
            print("An Error occured while matching " + str(player) + " with the library.")
            print("Make sure you are using the correct directory.")
            return []
    elif isinstance(library, dict):
        if player not in library:
            print("Player not in Library")
            return []
        library_embedding = library[player]
    else:
        print("Incorrect Library Input")
        return []

    # Crop all faces from the image and measure their distance from the library embeddings
    coordlist = []
    maxconvpercent = 0
    faces = cropped_faces_from_image(image)
    for face in faces:
        result = comparison_with_library(image, library_embedding, mtcnn, resnet)
        if result[0] > 0.65 and result[1] > 0.8 and result[0] * (result[1] ** 2) > maxconvpercent:
            maxconvpercent = result[0] * (result[1] ** 2)
            coordlist.append(face[1])
    return coordlist


class PlayerRegistration:
    def __init__(self, librarydirectory, imagesperlibrary=9, playernr=1, imagesize=160, margin=0.2):
        assert isinstance(librarydirectory, str)
        self.directory = librarydirectory
        assert isinstance(playernr, int)
        self._playernr = playernr
        assert isinstance(imagesperlibrary, int)
        self._imagesperlibrary = imagesperlibrary

        # Facenet Set-Up
        self._mtcnn, self._resnet = facenet_setup(imagesize, margin)

        # If there are already libraries registered in the current directory, add them to the embeddingslist
        self.libraryembeddings = {}
        if len(os.listdir(librarydirectory)) > 0:
            for i in os.listdir(librarydirectory):
                self.libraryembeddings[i] = library_embeddings(os.path.join(librarydirectory, i), self._mtcnn,
                                                                self._resnet)

    def registerplayer(self, player=None):
        assert player is None or isinstance(player, str) or isinstance(player, int)
        if player is None:
            player = str(player) + str(self._playernr)
        embeddings = create_player_library(player, self.directory, self._imagesperlibrary, self._mtcnn, self._resnet)
        if embeddings is not None and player not in self.libraryembeddings:
            self.libraryembeddings[player] = embeddings
        elif embeddings is not None:
            self.libraryembeddings[player] = self.libraryembeddings[player] + embeddings
        if player not in os.listdir(self.directory):
            self._playernr += 1

    def identifyface(self, image, libraryembeddings=None):
        if libraryembeddings is None:
            libraryembeddings = self.libraryembeddings
        assert isinstance(libraryembeddings, dict)
        image, matches = face_recognition(image, self._mtcnn, self._resnet, libraryembeddings)
        return image, matches

    def searchplayer(self, player, image, libraryembeddings=None):
        if libraryembeddings is None:
            libraryembeddings = self.libraryembeddings
        coordlist = search_player(player, image, self._mtcnn, self._resnet, libraryembeddings)
        return coordlist

    def get_directory(self):
        return self.directory

# Bram1 = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Bram1.jpg")
# Bram2 = Image.open(r'C:\Users\bram\facenetLibraries\Bram\image4.jpg')
# Karel = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Karel.jpg")
# print(embedding_matching(Bram1, Gorjan1))

#
# # print(image_matching(Bram2, Bram2))
# # print(comparison_with_library(Karel, r'C:\Users\bram\facenetLibraries\Bram'))


# print(looking_direction(Image.open(r'C:\Users\bram\facenetLibraries\Bram\image8.jpg')))


# library = PlayerRegistration(r'C:\Users\bram\facenetLibraries', 9)
# print(library.get_directory())
# # library.registerplayer("Bram")
# # #
# imagesize=160
# margin=0.2
# mtcnn, resnet = facenet_setup(imagesize, margin)
# # libraryembedding = {}
# # libraryembedding["Bram"] = library_embeddings(r'C:\Users\bram\facenetLibraries\Bram', mtcnn, resnet)
# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# # # instance = PlayerRegistration(r'C:\Users\bram\facenetLibraries')
# while True:
#     ret, img = cam.read()
#     # img, resultingmatches = library.identifyface(img, libraryembedding)
# #     print(resultingmatches)
#     print(library.searchplayer('Bram', img))
#     cv2.imshow("Face", img)
#     cv2.waitKey(1)
