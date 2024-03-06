from django.utils import timezone

from django.core import serializers
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from CameraApp.camera import VideoCamera 
from datetime import datetime, timedelta

import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth.hashers import check_password, make_password
from API.models import AuthenFaceUser
from API.serializers import AuthenFaceUserSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import jwt
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def gen(request, camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def video_feed(request):
    # TODO, get username/email
    user_name = 'EJ'

    return StreamingHttpResponse(gen(request, VideoCamera(user_name)),
        content_type='multipart/x-mixed-replace; boundary=frame')

def generate_jwt_token(user_id, email, expiration_time_minutes = 15):
    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_time_minutes)
    payload = {'id': user_id, 'email': email, 'exp' : expiration_time}
    jwt_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return jwt_token

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_object_or_404(AuthenFaceUser, email=email)
        if user and check_password(password, user.password):
            token = generate_jwt_token(user.id, user.email)
            userData = {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }

            return Response({'message': 'User registered successfully', 'token' : token, 'userData' : userData}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def create_image_name(name): # TODO fix this later
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f'{name.lower()}_profile_image_{timestamp}.png'

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        image_file = request.data.get('userImage')
        userName = request.data.get('name')
        password = request.data.get('password')
        userImageFileName = create_image_name(userName)
    
        if password != request.data.get('confirmPassword'):
            return Response({'error' : 'password did not match'}, status=status.HTTP_400_BAD_REQUEST)          

        try:
            validators.validate_password(password)
        except exceptions.ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        userInput = {
            'name': userName,
            'email': request.data.get('email'),
            'password': password,
            'userImageName': userImageFileName
        }

        serializer = AuthenFaceUserSerializer(data=userInput)

        if serializer.is_valid() and image_file:
            user = serializer.save()
            userObject = AuthenFaceUser.objects.get(id = user.id)
            userObject.password = make_password(user.password)
            userObject.save()
            token = generate_jwt_token(user.id, user.email)

            with open('Media/UserImages/' + userImageFileName, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            userData = {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }

            return Response({'message': 'User registered successfully', 'token' : token, 'userData' : userData}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error' : 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)  