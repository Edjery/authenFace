import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'cameraApp/images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
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

encodeListKnown = findEncodings(images)

def markAttendance(name):
    with open('Attendance.csv', 'r') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,1,1)
    
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceloc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceloc
            #y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Remove this line to draw on the original image
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # markAttendance(name)
    
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break



# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime

# class FaceRecognition:
#     def __init__(self):
#         self.path = 'cameraApp/images'
#         self.images = []
#         self.classNames = []
#         self.myList = os.listdir(self.path)
#         print(self.myList)

#         for cl in self.myList:
#             curImg = cv2.imread(f'{self.path}/{cl}')
#             self.images.append(curImg)
#             self.classNames.append(os.path.splitext(cl)[0])

#         self.encodeListKnown = self.findEncodings(self.images)

#     def findEncodings(self, images):
#         encodeList = []
#         for img in images:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             encode = face_recognition.face_encodings(img)[0]
#             encodeList.append(encode)
#         return encodeList

#     def recognize_faces(self, frame):
#         imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
#         facesCurFrame = face_recognition.face_locations(imgS)
#         encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#         for encodeFace, faceloc in zip(encodesCurFrame, facesCurFrame):
#             matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
#             print(faceDis)
#             matchIndex = np.argmin(faceDis)

#             if matches[matchIndex]:
#                 name = self.classNames[matchIndex].upper()
#                 print(name)
#                 y1, x2, y2, x1 = faceloc
#                 y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#                 cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#         return frame


# latest camera ----------------------------------------------

# import cv2
# import os
# import face_recognition
# import numpy as np
# from webApp2FA.models import WebsiteList, UserImage

# import os
# from django.conf import settings

# def get_selfieimage_path(image_filename):
#     # Construct the absolute file path to the image
#     media_root = settings.MEDIA_ROOT
#     selfieimage_path = os.path.join(media_root, 'selfieimage', image_filename)
#     return selfieimage_path

# class VideoCamera(object):
#     def __init__(self, request, currentUser):
#         self.video = cv2.VideoCapture(0)
#         self.currentUser = currentUser
#         self.request = request
#         self.match_value = None

#         self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))

#         def set_camera_resolution(cap, width, height):
#             cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#             cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#         # Set the desired resolution (e.g., 640x480)
#         desired_width = 340
#         desired_height = 280

#         # Set the camera resolution to the desired values
#         set_camera_resolution(self.video, desired_width, desired_height)
        
#         website = WebsiteList.objects.get(username=self.currentUser)
#         try:
#             user_image = UserImage.objects.get(userID=website.userID)
#         except UserImage.DoesNotExist:
#             user_image = None

#         path = user_image.userImage.url.lstrip('/')  # example: 'cameraApp/images/ed.png' 'media/selfieimages/ed_EYWq4vT.png'
#         # path = path.replace('/', '\\')
#         print(path)
#         images = []
#         self.classNames = []

#         curImg = cv2.imread(path)
#         images.append(curImg)

#         self.classNames.append(os.path.splitext(os.path.basename(path))[0])

#         print(self.classNames)  # Output: ['image1']
#         print(len(images))  # Output: 1
            
#         def findEncodings(images):  
#             encodeList = []
#             for img in images:
#                 img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#                 encode = face_recognition.face_encodings(img)[0]
#                 encodeList.append(encode)
#             return encodeList

#         self.encodeListKnown = findEncodings(images)

#     def __del__(self):
#         self.video.release()
        
#     # This function is used in views
#     def get_frame(self, request):
#         success, self.image = self.video.read()

#         facesCurFrame = face_recognition.face_locations(self.image)
#         encodesCurFrame = face_recognition.face_encodings(self.image,facesCurFrame)

#         for encodeFace,faceloc in zip(encodesCurFrame,facesCurFrame):
#                 matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
#                 faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
#                 # print(faceDis)
#                 matchIndex = np.argmin(faceDis)
                
#                 if matches[matchIndex]:
#                     name = self.classNames[matchIndex].upper()

#                     # print(name)
#                     y1, x2, y2, x1 = faceloc
#                     cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     # cv2.rectangle(self.image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#                     # cv2.putText(self.image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

#                     text = "Done, Click next"
#                     cv2.putText(self.image, text, (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

#                     # from webAppDummy.views import login as dummyLogin
#                     # return dummyLogin(self.request, name)
#                     request.session['match_value'] = self.currentUser

#         # Encode the frame as JPEG
#         ret, jpeg = cv2.imencode('.png', self.image)

#         return jpeg.tobytes()
    
#     # def get_match_value(self, value):
#     #     self.match_value = value
#     #     return value