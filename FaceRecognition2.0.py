from imutils import paths
import pickle
import cv2
import os
import numpy

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0)
directory = r'C:\Users\bram\testfolder\s'

def imagesizeconverter (x,y,w,h):
    width = 60
    height = 80
    if w != width or h != height:
        # We are gonna be using x+a and w-a to keep the center of the face in the center,
        # so now we have to find a to convert
        a = (w-width)/2
        b = (h-height)/2

        x += a
        y += b
    return [int(x), int(y), int(x+width), int(y+height)]

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

# get paths of each file in folder named Images
# Images here contains my data(folders of various persons)
face = 0
while True:
    ret,img=cam.read();  # Makes a giant array of pixels
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # Changes the array into grayscale
    faces=faceDetect.detectMultiScale(gray,1.3,5);  # This detects faces in a matrix
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x-20,y-20),(x+w+20,y+h+20),(0,255,0),2)  # This creates the rectangle around your face
        cv2.waitKey(1);  # This is a delay
        convertedimage = imagesizeconverter(x, y, w, h)
        vectornewface = numpy.array(gray[convertedimage[1]:convertedimage[3],
                                        convertedimage[0]:convertedimage[2]]).reshape(-1)
        weightvectornewface = numpy.dot(eigenfaces.transpose(), vectornewface - averageface)
        predefined_treshhold = 1000;
        match = 0;
        for i in range(len(os.listdir(r"C:\Users\bram\testfolder"))):
            euclidian_distance[i] = numpy.linalg.norm(weightvectornewface - (Eigenfaces.transpose()*difference_with_average_face[:,i]));
            if euclidian_distance[i] < predefined_treshhold:
                match += 1
            if match == len(os.listdir(r"C:\Users\bram\testfolder")):
                cv2.rectangle(img, (convertedimage[0], convertedimage[1]), (convertedimage[2], convertedimage[3]),
                              (255, 0, 0), 2)
            else:
                cv2.rectangle(img, (convertedimage[0], convertedimage[1]), (convertedimage[2], convertedimage[3]),
                              (0, 0, 255), 2)
    cv2.imshow("Face",img);  # This shows the camera image
    cv2.waitKey(1);
    face += 1
    if face == 1:
        break
cam.release()
cv2.destroyAllWindows()