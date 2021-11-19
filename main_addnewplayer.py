import cv2
import numpy as np
import os
import mediapipe as mp
from PIL import Image


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
    return directory


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


def normalise_lightlevel(imagematrix):
    median = np.median(imagematrix)
    differencefromnormal = 125 - median
    normalisedimage = imagematrix + differencefromnormal
    return normalisedimage


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
                cv2.circle(img, (x, y), 1, (0, 255, 0))
            if face_landmarks.landmark[454].x - face_landmarks.landmark[1].x < 1 / 3 * (
                    face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                return "Right", img
            elif face_landmarks.landmark[454].x - face_landmarks.landmark[1].x > 2 / 3 * (
                    face_landmarks.landmark[454].x - face_landmarks.landmark[234].x):
                return "Left", img
            else:
                return "Centered", img
    return None, img


def wheretostilllook(rlfaces, clfaces, llfaces, nofperlib, img):
    if rlfaces >= nofperlib and llfaces >= nofperlib:
        cv2.putText(img=img,text=str("Look Centered"),org=(0, 20),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.5,
            color=(0, 255, 0),thickness=1)
    elif rlfaces >= nofperlib and clfaces >= nofperlib:
        cv2.putText(img=img,text=str("Look Left"),org=(0, 20),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.5,
            color=(0, 255, 0),thickness=1)
    elif llfaces >= nofperlib and clfaces >= nofperlib:
        cv2.putText(img=img,text=str("Look Right"),org=(0, 20),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.5,
            color=(0, 255, 0),thickness=1)
    elif rlfaces >= nofperlib:
        cv2.putText(img=img,text=str("Look Centered or Left"),org=(0, 20),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.5,
            color=(0, 255, 0),thickness=1)
    elif llfaces >= nofperlib:
        cv2.putText(img=img,text=str("Look Centered or Right"),org=(0, 20),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.5,
                    color=(0, 255, 0),thickness=1)
    elif clfaces >= nofperlib:
        cv2.putText(img=img,text=str("Look Left or Right"),org=(0, 20),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.5,
            color=(0, 255, 0),thickness=1)
    return img


def libraryimprint(direction, new_directory, convertedimage, rightlookingfaces, centeredlookingfaces, leftlookingfaces, numberoffacesperlibrary):
    right_directory = createFolder(new_directory + str(r"\lookingRight"))
    centered_directory = createFolder(new_directory + str(r"\lookingCentered"))
    left_directory = createFolder(new_directory + str(r"\lookingLeft"))
    if direction == "Right" and rightlookingfaces < numberoffacesperlibrary:
        cv2.imwrite(str(right_directory) + str(r"\seenface") + str(rightlookingfaces) + ".jpg",
                    convertedimage)
        rightlookingfaces += 1
    elif direction == "Left" and leftlookingfaces < numberoffacesperlibrary:
        cv2.imwrite(str(left_directory) + str(r"\seenface") + str(leftlookingfaces) + ".jpg",
                    convertedimage)
        leftlookingfaces += 1
    elif centeredlookingfaces < numberoffacesperlibrary:
        cv2.imwrite(str(centered_directory) + str(r"\seenface") + str(centeredlookingfaces) + ".jpg",
                    convertedimage)
        centeredlookingfaces += 1
    else:
        pass
    return rightlookingfaces, centeredlookingfaces, leftlookingfaces


def singlefacelibrarymaker(new_directory, numberoffacesperlibrary, width = 30, height = 40):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    rightlookingfaces = 0
    centeredlookingfaces = 0
    leftlookingfaces = 0
    while True:
        ret, img = cam.read();  # Makes a giant array of pixels
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Changes the array into grayscale
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)  # This detects faces in a matrix
        for (x, y, w, h) in faces:
            if w >= width and h >= height:
                convertedimage = imagesizeconverter(x, y, w, h, gray, width, height)
                direction, img = lookingdirection(img)
                convertedimage = normalise_lightlevel(convertedimage)
                rightlookingfaces, centeredlookingfaces, leftlookingfaces = libraryimprint(direction, new_directory, convertedimage,
                                                                                           rightlookingfaces,
                                                                                           centeredlookingfaces,
                                                                                           leftlookingfaces,
                                                                                           numberoffacesperlibrary)
                img = wheretostilllook(rightlookingfaces, centeredlookingfaces, leftlookingfaces, numberoffacesperlibrary, img)
                # This stores the file on your computer
                cv2.rectangle(img, (x, y), (x+w, y+h),
                              (0, 255, 0), 2)  # This creates the rectangle around your face
                cv2.waitKey(1)  # This is a delay
        cv2.imshow("Face", img)  # This shows the camera image
        cv2.waitKey(1)
        if rightlookingfaces >= numberoffacesperlibrary and leftlookingfaces >= numberoffacesperlibrary and \
                centeredlookingfaces >= numberoffacesperlibrary:
            break
    cam.release()
    cv2.destroyAllWindows()


def __main_addnewplayer__(playernumber, directory, number_of_faces_per_library):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    new_directory = createFolder(directory + str(r"\player") + str(playernumber))
    print("Press Enter to engage library_create for player" + str(playernumber))
    while True:
        ret, img = cam.read()
        cv2.imshow("Face", img)
        if cv2.waitKey(1) & 0xff == 13:  # If you press Enter
            singlefacelibrarymaker(new_directory, number_of_faces_per_library)
            break
        elif cv2.waitKey(1) & 0xff == 27:  # If you press Escape
            print("Disengaging library_create for player" + str(playernumber))
            break


class addPlayer:
    def __init__(self, directory, imagesperlibrary=50, playernumber=1):
        self.directory = directory
        self.currentplayernumber = playernumber
        self.imagesperlibrary = imagesperlibrary

    def add_newplayer(self, playernumber=None):
        isNone = 0
        if playernumber is None:
            playernumber = self.currentplayernumber
            isNone = 1
        __main_addnewplayer__(playernumber, self.directory, self.imagesperlibrary)
        if isNone == 1:
            self.currentplayernumber += 1
        return True


# library = addPlayer(r'C:\Users\bram\testfolder', 2, 1)
# library.add_newplayer()
# library.add_newplayer(5)

