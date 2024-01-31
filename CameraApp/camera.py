from django.conf import settings
import os
import numpy as np
import cv2
import face_recognition

class VideoCamera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.match = False
        
        self.user_image_name = 'EJ.jpg'
        path = os.path.join(settings.MEDIA_ROOT, 'UserImages')
        user_image_path = os.path.join(path, self.user_image_name)
        
        user_image = face_recognition.load_image_file(user_image_path)
        image_face_locations = face_recognition.face_locations(user_image)

        self.face_encodings = []
        if image_face_locations:
            self.face_encodings = face_recognition.face_encodings(user_image, image_face_locations)[0]
            print('Encoding complete.')
        else:
            print('No Face Located')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        currrent_face_location = face_recognition.face_locations(frame)

        if currrent_face_location:
            current_face_encoding = face_recognition.face_encodings(frame, currrent_face_location)
            matches = face_recognition.compare_faces(self.face_encodings, current_face_encoding)
            face_distance = face_recognition.face_distance(self.face_encodings, current_face_encoding)
            match_index = np.argmin(face_distance)

        for y1, x2, y2, x1 in currrent_face_location:
                if (matches[match_index]): 
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 
                    self.match = True
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) 
                    self.match = False

        flip_frame = cv2.flip(frame, 1) # Flips camera so that it will show a mirror instead
        _, jpeg = cv2.imencode('.jpeg', flip_frame)
        return jpeg.tobytes()