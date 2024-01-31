import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        uccess, frame = self.video.read()

        frame_flip = cv2.flip(frame,1) # Flips camera so that it will show a mirror instead
        _, jpeg = cv2.imencode('.jpeg', frame_flip)
        return jpeg.tobytes()