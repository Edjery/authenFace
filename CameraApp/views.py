import os
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from API.models import AuthenFaceUser, Snapshot
from CameraApp.camera import VideoCamera 

def index(request, data = None):
    context = {}
    
    if data:
        context['email'] = request.GET.get('email', '')
        context['redirect_url'] = request.GET.get('redirect_url', '')
        return render(request, 'index.html', context)
    else:
        return render(request, 'error.html', context)
    

def gen(request, camera: VideoCamera):
    global match, redirect_url, current_user, snapshot_path, snapshot_name, frame, user_email
    while True:
        frame = camera.get_frame()

        current_user = camera.user
        match = camera.match
        redirect_url = camera.redirect_url
        snapshot_path = camera.snapshot_path
        snapshot_name = camera.snapshot_name
        user_email = camera.email
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    email = request.GET.get('email', '')
    redirect_url = request.GET.get('redirect_url', '')

    return StreamingHttpResponse(gen(request, VideoCamera(email, redirect_url)),
        content_type='multipart/x-mixed-replace; boundary=frame')

def delete_file(imagePath):
    try:
        os.remove(imagePath)
        print(f"{imagePath} has been deleted.")
    except OSError as e:
        print(f"Error deleting {imagePath}: {e}")

def generate_jwt_token(email, expiration_time_minutes = 30):
    expiration_time = datetime.now() + timedelta(minutes=expiration_time_minutes)
    payload = {'email': email, 'exp' : expiration_time}
    jwt_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return jwt_token

def authenticate(request):
    try:
        required_inputs = [redirect_url, current_user, snapshot_path, snapshot_name, frame, user_email]
        missing_inputs = [field for field in required_inputs if request.GET.get(field) == None]
    except:
        return render(request, 'error.html')
    
    try:
        user = get_object_or_404(AuthenFaceUser, email = current_user.email)

        if match is None or match is False:
            print('creating snapshot...')
            new_snapshot = Snapshot(name = snapshot_name, user = user, image = snapshot_path)
            new_snapshot.save()
            return redirect(redirect_url)
    except NameError:
        user = get_object_or_404(AuthenFaceUser, email = current_user.email)
        print('creating snapshot...')

        new_snapshot = Snapshot(name = snapshot_name, user = user)
        new_snapshot.save()
        return redirect(redirect_url)
    
    try:
        delete_file(snapshot_path)

        print('generating token...')

        token = generate_jwt_token(user_email)
        code = 'secretcodexyz'

        redirect_url_with_token = f"{redirect_url}?token={token}&code={code}"
        return redirect(redirect_url_with_token)
    except:
        return render(request, 'error.html')
