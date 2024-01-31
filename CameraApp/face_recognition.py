# import face_recognition
from django.conf import settings

def init_face_recognition():
    path = settings.MEDIA_ROOT
    return path