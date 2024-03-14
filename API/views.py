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
        user_id = self.kwargs.get('user_id') 
        if user_id is not None:
            return Website.objects.filter(user=user_id)
        else:
            return Website.objects.all()
    
class SnapshotListByUser(generics.ListAPIView):
    serializer_class = SnapshotSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id') 
        if user_id is not None:
            return Snapshot.objects.filter(user=user_id)
        else:
            return Snapshot.objects.all()