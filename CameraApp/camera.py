from django.utils import timezone
from django.conf import settings
import os
import numpy as np
import cv2
import face_recognition
from AntiSpoofingApp.test import test

class VideoCamera():
    def __init__(self, user_image_filename):
        self.video = cv2.VideoCapture(0)
        self.match = False

        self.user_image_filename = user_image_filename
        path = os.path.join(settings.MEDIA_ROOT, 'UserImages')
        user_image_path = os.path.join(path, self.user_image_filename)
        
        user_image = face_recognition.load_image_file(user_image_path)
        image_face_locations = face_recognition.face_locations(user_image)

        self.face_encodings = []
        if image_face_locations:
            self.face_encodings = face_recognition.face_encodings(user_image, image_face_locations)[0]
            print('Encoding complete.')
        else:
            print('No Face Located')

        self.snapshot_filename = ''
        self.snapshot_path = ''

    def test_face(self, frame):
        label = test(
                    image=frame,
                    model_dir=os.path.join(settings.BASE_DIR, 'AntiSpoofingApp\\resources\\anti_spoof_models'),
                    device_id=0
                )
        is_real_face = True if label == 1 else False
        return is_real_face

    def __del__(self):
        self.video.release()

    def capture_and_save_image(self, frame):
        print('Taking Snapshot')
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        # fileName = f"{self.website.userID}_temp_image_{timestamp}.png"
        self.snapshot_filename = f"_temp_image_{timestamp}.png"
        print('Snapshot Taken: ' + self.snapshot_filename)

        self.snapshot_path = os.path.join(settings.MEDIA_ROOT, 'Snapshots', self.snapshot_filename)
        print("Inserted in directory:", self.snapshot_path)

        # Capture and save the image using OpenCV
        success = cv2.imwrite(self.snapshot_path, frame)
        print("Snapshot Taken:", success)

    def get_frame(self):
        success, frame = self.video.read()
        is_real_face = self.test_face(frame)
        currrent_face_location = face_recognition.face_locations(frame)

        if currrent_face_location:
            current_face_encoding = face_recognition.face_encodings(frame, currrent_face_location)
            matches = face_recognition.compare_faces(self.face_encodings, current_face_encoding, 0.5)
            face_distance = face_recognition.face_distance(self.face_encodings, current_face_encoding)
            match_index = np.argmin(face_distance)

            for y1, x2, y2, x1 in currrent_face_location:
                    if (matches[match_index] and is_real_face): 
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 
                        self.match = True
                        # TODO, add return ok response then get back, add timeout too
                        # return these self.snapshot_filename, self.snapshot_path, self.match, 
                    else:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) 
                        self.match = False
                        self.capture_and_save_image(frame)
                        # TODO, add return bad response then get back, add timeout too


        flip_frame = cv2.flip(frame, 1) # Flips camera so that it will show a mirror instead
        _, jpeg = cv2.imencode('.jpeg', flip_frame)
        return jpeg.tobytes()