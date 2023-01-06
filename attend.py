import cv2
import numpy as np
import face_recognition
import os
import webbrowser
#import mysql.connector
from datetime import datetime
import webbrowser
#from jinja2 import Environment, FileSystemLoader, select_autoescape

"""
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
template = env.get_template("Secondpage.html")
print(template.render(thing='Hi there'))
webbrowser.open_new('Secondpage.html')
"""

path = 'Images'
images = []
classNames = []
List1 = os.listdir(path)

for cl in List1:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

"""
def mysqlconnection():
    connect = mysql.connector.connect(host='localhost', database='records', user='root', password='root')
    cursor = connect.cursor()
    cursor.execute("select * from year2")
    result = cursor.fetchall()
    for x in result:
        print(x)
"""

def markAttendance(name):
    with open('attend1.csv','w+') as k:
        myDataList = k.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S:%D')
            k.writelines(f'\n{name},{dtString}')
        if True:
            cv2.destroyAllWindows()
            webbrowser.open_new_tab('attendence.html')
            exit()

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)



    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
