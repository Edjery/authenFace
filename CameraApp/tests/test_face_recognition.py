
from CameraApp.face_recognition import init_face_recognition


class TestFaceRecognition:
    def test_face_init(self):
        path = init_face_recognition()
        assert str(path) == 1 