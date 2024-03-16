import os
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.core.files import File
from django.core import exceptions
import django.contrib.auth.password_validation as validators

from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .pagination import DefaultPagination
from .serializers import AuthenFaceUserSerializer, SnapshotSerializer, WebsiteSerializer, DummyUserSerializer
from .models import AuthenFaceUser, Snapshot, Website, DummyUser

# TODO add a view template to list all apis

def generate_jwt_token(user_id, email, expiration_time_minutes = 15):
    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_time_minutes)
    payload = {'id': user_id, 'email': email, 'exp' : expiration_time}
    jwt_token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return jwt_token

class UsersViewSet(ModelViewSet): 
    queryset = AuthenFaceUser.objects.all()
    serializer_class = AuthenFaceUserSerializer

    def create(self, request, *args, **kwargs):
        imageFile = request.data.get('userImage')
        password = request.data.get('password')
    
        if password != request.data.get('confirmPassword'):
            return Response({'error' : 'password did not match'}, status=status.HTTP_400_BAD_REQUEST)          
        try:
            validators.validate_password(password)
        except exceptions.ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        userInput = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': password,
            'image': imageFile
        }

        serializer = AuthenFaceUserSerializer(data=userInput)

        if serializer.is_valid() and imageFile:
            user = serializer.create(serializer.validated_data)
            token = generate_jwt_token(user.id, user.email)
            userData = {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
            return Response({'message': 'User registered successfully', 'token': token, 'userData': userData}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnapshotViewSet(ModelViewSet): 
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer
    pagination_class = DefaultPagination

class WebsiteViewSet(ModelViewSet): 
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    pagination_class = DefaultPagination

class DummyUserViewSet(ModelViewSet): 
    queryset = DummyUser.objects.all()
    serializer_class = DummyUserSerializer

class WebsiteListByUser(generics.ListCreateAPIView):
    serializer_class = WebsiteSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        userId = self.kwargs.get('userId') 
        if userId is not None:
            return Website.objects.filter(user=userId)
        else:
            return Website.objects.all()
    
class SnapshotListByUser(generics.ListAPIView):
    serializer_class = SnapshotSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        fileImageName = 'EJ.png_temp_image_20240315015853.png'
        userId = self.kwargs.get('userId') 
        if userId is not None:
            user = AuthenFaceUser.objects.get(id=userId)
            # generate_snapshot(fileImageName, user)
            return Snapshot.objects.filter(user=userId)
        else:
            return Snapshot.objects.all()

def generate_snapshot(imageFilename, user):
    imagePath = os.path.join(settings.MEDIA_ROOT, 'TempImages', imageFilename)
    
    if not os.path.exists(imagePath):
        print(f"Image file '{imageFilename}' not found in MEDIA_ROOT.")
        return None
    
    with open(imagePath, 'rb') as imageFIle:
        snapshot = Snapshot(name=imageFilename, user=user)
        snapshot.image.save(imageFilename, File(imageFIle))
        snapshot.save()
        
        return snapshot