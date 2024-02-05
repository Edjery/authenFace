from rest_framework.viewsets import ModelViewSet
from .pagination import DefaultPagination
from .serializers import AuthenFaceUserSerializer, UserImageSerializer, SnapshotSerializer, WebsiteSerializer, DummyUserSerializer
from .models import AuthenFaceUser, UserImage, Snapshot, Website, DummyUser

class UsersViewSet(ModelViewSet): 
    queryset = AuthenFaceUser.objects.all()
    serializer_class = AuthenFaceUserSerializer

class UserImageViewSet(ModelViewSet): 
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer

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