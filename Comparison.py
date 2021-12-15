from facenet_facerecognition import PlayerRegistration
from main_facerecognition import face_recognition
import numpy as np
from PIL import Image
import os

eigenrecog = face_recognition(r'C:\Users\bram\testfolder')
facenetrecog = PlayerRegistration(r'C:\Users\bram\facenetLibraries')

testimgdir = r'C:\Users\bram\OneDrive\Documenten\2Bbi KU Leuven\PnO3\TestFotos'

Bram1 = Image.open(r"C:\Users\bram\OneDrive\Afbeeldingen\Camera-album\Bram1.jpg")

correct = {'eigen': 0, 'facenet': 0}
none = {'eigen': 0, 'facenet': 0}

for folder in os.listdir(testimgdir):
    for image in os.listdir(os.path.join(testimgdir, folder)):
        expectedoutput = folder
        testimg = np.array(Image.open(os.path.join(testimgdir, os.path.join(folder, image))))
        img, eigenface = eigenrecog.faceRecognition(testimg)
        img, facenet = facenetrecog.identifyface(testimg)
        print('eigenfaces: ', eigenface, 'facenet: ', facenet, 'expected: ', expectedoutput)
        if not eigenface:
            none['eigen'] += 1
        elif eigenface[0][1] == expectedoutput:
            correct['eigen'] += 1
        if not facenet or facenet[0][1] is None:
            none['facenet'] += 1
        elif facenet[0][1] == expectedoutput:
            correct['facenet'] += 1
print('correct: ', correct)
print('none recognised: ', none)
