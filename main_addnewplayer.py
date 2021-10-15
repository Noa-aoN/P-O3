import cv2
import numpy as np
import os

directory = r'C:\Users\bram\testfolder'

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0)
width = 60
height = 80
playernumber = 1
number_of_faces_per_library = 20


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
    return directory


def imagesizeconverter(x, y, w, h):
    if w != width or h != height:
        # We are gonna be using x+a and w-a to keep the center of the face in the center,
        # so now we have to find a to convert
        a = (w - width) / 2
        b = (h - height) / 2

        x += a
        y += b
    return [int(x), int(y), int(x + width), int(y + height)]


def singlefacelibrarymaker(new_directory, numberoffacesperlibrary):
    face = 0
    while True:
        ret, img = cam.read();  # Makes a giant array of pixels
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Changes the array into grayscale
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)  # This detects faces in a matrix
        for (x, y, w, h) in faces:
            face += 1  # This stores amount of samples
            convertedimage = imagesizeconverter(x, y, w, h)
            cv2.imwrite(str(new_directory) + str(r"\seenface") + str(face) + ".jpg",
                        gray[convertedimage[1]:convertedimage[3],
                        convertedimage[0]:convertedimage[2]])
            # This stores the file on your computer
            cv2.rectangle(img, (convertedimage[0], convertedimage[1]), (convertedimage[2], convertedimage[3]),
                          (0, 255, 0), 2)  # This creates the rectangle around your face
            cv2.waitKey(1)  # This is a delay
        cv2.imshow("Face", img)  # This shows the camera image
        cv2.waitKey(1)
        if face > numberoffacesperlibrary:
            break
    cam.release()
    cv2.destroyAllWindows()


def __main__():
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


__main__()
