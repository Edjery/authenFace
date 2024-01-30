import os, numpy as np
import cv2, face_recognition

from django.conf import settings
from django.utils import timezone

from webApp2FA.models import WebsiteList, UserImage
from antiSpoofingApp.test import test

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

class VideoCamera(object):
    def __init__(self, currentUser, website_url):
        self.video = cv2.VideoCapture(0)
        self.currentUser = currentUser
        self.website_url = website_url
        self.imageCaptured = False # For capturing intruder Images

        self.match = False
        self.fileName = ''
        self.imagePath = ''

        # Loading the user's image
        self.website = WebsiteList.objects.filter(websiteUrl=self.website_url, username=self.currentUser).first()
        try:
            user_image = UserImage.objects.get(userID=self.website.userID)
            user_image_name = os.path.basename(user_image.userImage.name) # name of the image file

        except UserImage.DoesNotExist:
            user_image = None
            user_image_name = ''

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        user_image_path = os.path.join(parent_dir, 'media', 'selfieimages', user_image_name)

        image = face_recognition.load_image_file(user_image_path)

        # Perform face detection
        face_locations = face_recognition.face_locations(image)

        # Encoding Process
        if face_locations:
            self.faceEncodings = face_recognition.face_encodings(image, face_locations)[0]
            print('Encoding complete.')


    def __del__(self):
        self.video.release()

    def antiSpoof(self, frame):
        # Get the directory of the script that's currently running
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

        # Define the relative path to the directory you want to access
        relative_path = 'antiSpoofingApp\\resources\\anti_spoof_models'

        label = test(
                    image=frame,
                    model_dir=os.path.join(parent_dir, relative_path),
                    device_id=0
                )
        # label = 1 means Real person
        # label = 2 means Fake person

        return label
    
    def capture_and_save_image(self, frame):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        fileName = f"{self.website.userID}_temp_image_{timestamp}.png"
        print('intruder pic name: ' + fileName)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        imagePath = os.path.join(parent_dir, 'media', 'intruderimages', fileName)
        print("Current directory:", imagePath)

        # Capture and save the image using OpenCV
        success = cv2.imwrite(imagePath, frame)
        print(f"Photo pic: {success}")
        return fileName, imagePath

    def get_frame(self):
        success, frame = self.video.read()
        
        label = self.antiSpoof(frame)

        if self.imageCaptured == False:
            self.fileName, self.imagePath = self.capture_and_save_image(frame)
            self.imageCaptured = True
            print('taking pic')

        # Face Recognition process starts here
        currrentFaceLocation = face_recognition.face_locations(frame)
        for y1, x2, y2, x1 in currrentFaceLocation:
            if currrentFaceLocation: # checks if there are any faces
                currentFaceEncoding = face_recognition.face_encodings(frame, currrentFaceLocation)

                matches = face_recognition.compare_faces(self.faceEncodings, currentFaceEncoding)
                faceDis = face_recognition.face_distance(self.faceEncodings, currentFaceEncoding)
                matchIndex = np.argmin(faceDis)

                if (matches[matchIndex] and label == 1): 
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 
                    self.match = True
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) 
                    self.match = False

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the video stream.

        frame_flip = cv2.flip(frame,1) # Flips camera so that it will show a mirror instead
        _, jpeg = cv2.imencode('.jpg', frame_flip)
        return self.fileName, self.imagePath, self.match, jpeg.tobytes()