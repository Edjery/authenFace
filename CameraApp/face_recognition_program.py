import face_recognition
import os
import cv2
from django.conf import settings
import numpy as np

def init_face_recognition():
    path = os.path.join(settings.MEDIA_ROOT, 'UserImages')
    list_of_files_in_path = os.listdir(path)

    image_file_names = []
    images = []
    for file_name in list_of_files_in_path:
        image_file_names.append(os.path.splitext(file_name)[0])
        image = cv2.imread(f'{path}/{file_name}') # images are converted to numpy array
        images.append(image)

    encoded_faces = []
    for image in images:
        convert_image_color = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Converts Color (Blue, Green, Red) to (Red, Green, Blue).
        encode = face_recognition.face_encodings(convert_image_color)
        encoded_faces.append(encode)
    
    return image_file_names, encoded_faces 

image_file_names, encoded_faces = init_face_recognition()

camera = cv2.VideoCapture(0)

def get_face_locations_and_encodings(frame):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    return face_locations, face_encodings

def get_matching_face(encoded_faces, encoded_face):
    matches = face_recognition.compare_faces(encoded_faces, encoded_face)
    distances = face_recognition.face_distance(encoded_faces, encoded_face)
    match_index = np.argmin(distances)
    return matches, match_index

def draw_face_info(frame, face_location, name):
    y1, x2, y2, x1 = face_location
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

def process_faces(frame, image_file_names, encoded_faces):
    current_face_locations, current_face_encodings =  get_face_locations_and_encodings(frame)

    for encoded_face, face_location in zip(current_face_encodings, current_face_locations):
        matches, match_index = get_matching_face(encoded_faces, encoded_face)
        
        if matches[match_index]:
            current_image_file_name = image_file_names[match_index].upper()
            print('Currrent image file name:', current_image_file_name)
            draw_face_info(frame, face_location, current_image_file_name)

# while True:
#     success, frame = camera.read()
#     resized_camera = cv2.resize(frame, (0,0), None, 1, 1)
#     process_faces(frame, image_file_names, encoded_faces)
#     cv2.imshow('Webcam', frame)
#     cv2.waitKey(1)
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break

# notes
# can you remove the convertion of color?
# can you use the load_image_file of face recognition instead of cv2's?