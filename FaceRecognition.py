import cv2
import numpy as np
import sqlite3

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);

def insertOrUpdate(Id,Name,Age,Gen,CR):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name="+str(Name)+"WHERE ID="+str(Id)
        cmd2="UPDATE People SET Age="+str(Age)+"WHERE ID="+str(Id)
        cmd3="UPDATE People SET Gender="+str(Gen)+"WHERE ID="+str(Id)
        cmd4="UPDATE People SET CR="+str(CR)+"WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO People(ID,Name,Age,Gender,CR) Values("+str(Id)+","+str(Name)+","+str(Age)+","+str(Gen)+","+str(CR)+")"
        cmd2=""
        cmd3=""
        cmd4=""
    conn.execute(cmd)
    conn.execute(cmd2)
    conn.execute(cmd3)
    conn.execute(cmd4)
    conn.commit()
    conn.close()



sampleNum=0
while(True):
    ret,img=cam.read();  # Makes a giant array of pixels
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # Changes the array into grayscale
    faces=faceDetect.detectMultiScale(gray,1.3,5);  # This detects faces in a matrix
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1;  # This stores amount of samples
        cv2.imwrite("dataSet/User."+str('lol')+"."+str(sampleNum)+".jpg",gray[y-20:y+h+20,x-20:x+w+20])
        cv2.rectangle(img,(x-20,y-20),(x+w+20,y+h+20),(0,255,0),2)  # This creates the rectangle around your face
        cv2.waitKey(100);
    cv2.imshow("Face",img);
    cv2.waitKey(1);
    if(sampleNum>20):
        break;
cam.release()
cv2.destroyAllWindows()
