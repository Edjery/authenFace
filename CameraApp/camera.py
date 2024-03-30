import os
import numpy as np
import cv2
import face_recognition

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings

from API.models import Website
from AntiSpoofingApp.test import test

camera_threshold = 0.6
class VideoCamera():
    def __init__(self, user_email, redirect_url):
        print('init camera...')
        self.video = cv2.VideoCapture(0)
        self.email = user_email
        self.redirect_url = redirect_url
        self.match = None

        self.snapshotTaken = False
        self.snapshot_name = ''
        self.snapshot_filename = ''
        self.snapshot_path  = ''

        self.website = None
        self.user = None

        print('finding user...')
        try:
            self.website = get_object_or_404(Website, account_name=self.email)
            self.user = self.website.user
        except Website.DoesNotExist:
            print("error in finding user")
        
        if (self.website == None):
            print("error in finding user")
        
        image = self.website.user.image

        print('finding image...')
        path = os.path.join(settings.MEDIA_ROOT)
        user_image_path = os.path.join(path, str(image))
        
        print('loading image...')
        user_image = face_recognition.load_image_file(user_image_path)
        image_face_locations = face_recognition.face_locations(user_image)

        self.face_encodings = []
        if image_face_locations:
            self.face_encodings = face_recognition.face_encodings(user_image, image_face_locations)[0]
            print('Encoding complete.')
        else:
            print('No Face Located')

    def test_face(self, frame):
        label = test(
                    image=frame,
                    model_dir=os.path.join(settings.BASE_DIR, 'AntiSpoofingApp\\resources\\anti_spoof_models'),
                    device_id=0
                )
        return True if label == 1 else False

    def __del__(self):
        self.video.release()

    def capture_and_save_image(self, frame):
        print('Taking Snapshot')
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        self.snapshot_name = f'{self.website.user.name}_snapshot_{timestamp}.png'
        self.snapshot_filename = f'{self.website.user.name}_temp_image_{timestamp}.png'
        print('Snapshot Taken: ' + self.snapshot_filename)
        self.snapshot_path = os.path.join(settings.MEDIA_ROOT, 'TempImages', self.snapshot_filename)
        print('Inserted in directory:', self.snapshot_path)
        success = cv2.imwrite(self.snapshot_path, frame)
        print('Snapshot Taken:', success)

    def get_frame(self):
        success, frame = self.video.read()
        is_real_face = self.test_face(frame)
        currrent_face_location = face_recognition.face_locations(frame)

        if self.snapshotTaken == False:
            self.snapshotTaken = True
            self.capture_and_save_image(frame)

        if currrent_face_location:
            current_face_encoding = face_recognition.face_encodings(frame, currrent_face_location)
            matches = face_recognition.compare_faces(self.face_encodings, current_face_encoding, camera_threshold)
            face_distance = face_recognition.face_distance(self.face_encodings, current_face_encoding)
            match_index = np.argmin(face_distance)

            for y1, x2, y2, x1 in currrent_face_location:
                if (matches[match_index] and is_real_face): 
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 
                    self.match = True

                else:        
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) 
                    self.match = False


        flip_frame = cv2.flip(frame, 1) # Flips camera so that it will show a mirror instead
        _, jpeg = cv2.imencode('.jpeg', flip_frame)
        return jpeg.tobytes()