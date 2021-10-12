from PIL import Image
import numpy as np
import cv2

cam = cv2.VideoCapture(0)
face = 0
while True:
    ret, img = cam.read()
    print(img)
    width, height = img.size()
    for i in range(0, width):  # process all pixels
        for j in range(0, height):
            data = img.getpixel((i, j))
            # print(data) #(255, 255, 255)
            if data[0] == 255 and data[1] == 255 and data[2] == 255:
                img.putpixel((i, j), (44, 44, 44))
    cv2.imshow("Face", blackAndWhiteImage);  # This shows the camera image
    cv2.waitKey(1);
    face += 1
    if face == 1000:
        break