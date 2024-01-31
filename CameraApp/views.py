from django.http import StreamingHttpResponse
from django.shortcuts import render
from CameraApp.camera import VideoCamera 

def index(request):
    return render(request, 'index.html')

def gen(request, camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def video_feed(request):
    user_image_filename = 'EJ.jpg'
    # TODO, get user image file name

    return StreamingHttpResponse(gen(request, VideoCamera(user_image_filename)),
        content_type='multipart/x-mixed-replace; boundary=frame')