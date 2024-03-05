from django.utils import timezone

from django.http import StreamingHttpResponse
from django.shortcuts import render
from CameraApp.camera import VideoCamera 

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

def generate_jwt_token(user_id, email):
    payload = {'id': user_id, 'email': email}
    jwt_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return jwt_token

@api_view(['POST'])
def login_user (request):
    pass
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = get_object_or_404(AuthenFaceUser, email=email)
#         if user and check_password(password, user.password):
#             login(request, user)
#             return JsonResponse({'success': True, 'message': 'Login successful'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=400)
#     else:
#         return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'}, status=405)

def create_image_name(name): # TODO fix this later
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f'{name}_profile_image_{timestamp}.png'

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        if request.data.get('password') != request.data.get('confirmPassword'):
            return Response({'error' : 'password did not match'}, status=status.HTTP_400_BAD_REQUEST)          

        image_file = request.data.get('userImage')
        userName = request.data.get('name')
        userImageFileName = create_image_name(userName)

        userData = {
            'name': userName,
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'userImageName': userImageFileName
        }

        serializer = AuthenFaceUserSerializer(data=userData)

        if serializer.is_valid() and image_file:
            user = serializer.save()
            userObject = AuthenFaceUser.objects.get(id = user.id)
            userObject.password = make_password(user.password)
            userObject.save()
            print('password', userObject.password)
            token = generate_jwt_token(user.id, user.email)

            with open('Media/UserImages/' + userImageFileName, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            return Response({'message': 'User registered successfully', 'token' : token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error' : 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)  