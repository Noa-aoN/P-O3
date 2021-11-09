### **Problem 1) Lighting Issues (not per se a problem)**

`Solution 1:` Taking the lowest value in the grayimage matrix and subtracting all other values in the grayimagematrix by that number to 'normalise' the lighting level of each picture (necessary during both the librarycreation AND the facedetection)

### **Problem 2) Sizing Issue for the imagesnippets of each face**

`Solution 1:` Adding an extra check to the facedetection that ignores faces with width and/or height values below the wanted size and resizing all snippets to the wanted size by ignoring some values in the imagematrix (deleting rows and columns of pixels in fixed intervals depending on the sizedifference)

`Solution 2:` Estimating the distance between the camera and the person to try to convert the picture in that way.
### **Problem 3) Rotation of Faces**

`Solution 1:` By combining KeypointDetection in faces with the librarycreating program and the facerecognition program we can try to detect what way someone is looking when the picture was taken (you can do this by looking at the coordinates of the nose and the cheekbones; if the nose is left from both cheekbones you are looking left, if its in the middle they are looking straight etc.). Then we can create new libraries within the existing 'playerx' libraries for looking left, right or centered. As a bonus you can write the program in a way that evenly takes pictures of each lookingdirection (f.e. 50 images looking left, 50 images looking centered and 50 images looking right).

### **Problem 4) Face Recognition not identifying someone correctly**

`Solution 1:`By testing every library on each face, we can try to calculate the chance that it is a certain person. Then that person will be identified based on the library that has the highest probability to match. This can be done based on the average/median/minimum/maximum euclidian distance per library. The better a library seems to match with a face, the higher the probability of it being that person. Note: you will still have to determine a threshold that decides whether the person is actually a match or not, i.e. if the highest matchrate of a library with that person is 20%, then the person is probably in none of the libraries.

`Solution 2:`Having more diverse samples in each library, by checking if an image is too resemblant to the previously taken image during the librarycreation.