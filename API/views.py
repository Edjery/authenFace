import os
from django.conf import settings
from django.core.files import File
from django.http import FileResponse, HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from .pagination import DefaultPagination
from .serializers import AuthenFaceUserSerializer, SnapshotSerializer, WebsiteSerializer, DummyUserSerializer
from .models import AuthenFaceUser, Snapshot, Website, DummyUser

# TODO add a view template to list all apis

class UsersViewSet(ModelViewSet): 
    queryset = AuthenFaceUser.objects.all()
    serializer_class = AuthenFaceUserSerializer

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